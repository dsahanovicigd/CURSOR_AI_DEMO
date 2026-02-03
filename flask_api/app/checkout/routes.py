"""Checkout routes"""
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.checkout import checkout_bp
from app import db
from app.models import Cart, CartItem, Order, OrderItem, Product
from app.schemas.order import CheckoutSchema, OrderSchema
from marshmallow import ValidationError
from decimal import Decimal
from datetime import datetime


checkout_schema = CheckoutSchema()
order_schema = OrderSchema()


def validate_card_number(card_number):
    """Validate card number using Luhn algorithm"""
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10 == 0


def validate_card_expiry(month, year):
    """Validate card expiry date"""
    if not (1 <= month <= 12):
        return False
    expiry_date = datetime(year, month, 1)
    return expiry_date > datetime.now()


def process_payment_mock(payment_data, amount):
    """
    Mock payment processing service - simulates payment gateway behavior
    This is a fully mocked service for development/testing purposes.
    Replace with actual payment gateway integration in production.
    """
    import random
    
    # Extract payment data
    card_number = payment_data.get('card_number', '').replace(' ', '').replace('-', '')
    expiry_month = int(payment_data.get('expiry_month', 0))
    expiry_year = int(payment_data.get('expiry_year', 0))
    cvv = payment_data.get('cvv', '')
    
    # Validate card number
    if not card_number or len(card_number) < 13:
        return {
            'success': False,
            'error': 'Invalid card number',
            'error_code': 'INVALID_CARD'
        }
    
    # Validate card number using Luhn algorithm
    if not validate_card_number(card_number):
        return {
            'success': False,
            'error': 'Invalid card number (Luhn check failed)',
            'error_code': 'INVALID_CARD'
        }
    
    # Validate expiry
    if not expiry_month or not expiry_year:
        return {
            'success': False,
            'error': 'Expiry date is required',
            'error_code': 'INVALID_EXPIRY'
        }
    
    if not validate_card_expiry(expiry_month, expiry_year):
        return {
            'success': False,
            'error': 'Card has expired',
            'error_code': 'EXPIRED_CARD'
        }
    
    # Validate CVV
    if not cvv or len(cvv) not in [3, 4]:
        return {
            'success': False,
            'error': 'Invalid CVV (must be 3 or 4 digits)',
            'error_code': 'INVALID_CVV'
        }
    
    # Mock payment processing delay (simulate network call)
    # In production, this would be an actual API call to payment gateway
    
    # Mock successful payment - generate transaction ID
    transaction_id = f'TXN-{datetime.now().strftime("%Y%m%d")}-{random.randint(1000, 9999)}'
    
    # Log mock payment (in production, this would be logged to payment service)
    print(f"[MOCK PAYMENT] Processing payment of ${amount}")
    print(f"[MOCK PAYMENT] Transaction ID: {transaction_id}")
    print(f"[MOCK PAYMENT] Card ending in: {card_number[-4:]}")
    
    return {
        'success': True,
        'transaction_id': transaction_id,
        'amount': float(amount),
        'payment_method': 'credit_card',
        'status': 'approved'
    }


@checkout_bp.route('/process-payment', methods=['POST'])
@jwt_required()
def process_payment():
    """
    Process payment and create order
    Uses mocked payment service for development/testing
    """
    try:
        data = checkout_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'messages': err.messages}), 400
    
    user_id = get_jwt_identity()
    
    # Get user's cart
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404
    
    if cart.items.count() == 0:
        return jsonify({'error': 'Cart is empty'}), 400
    
    # Calculate totals
    subtotal = cart.calculate_subtotal()
    discount_amount = Decimal('0.00')
    
    if cart.discount_code and cart.discount_code.is_valid():
        discount_amount = cart.discount_code.calculate_discount(subtotal)
    
    # Calculate tax (8% example)
    tax_rate = Decimal('0.08')
    tax = subtotal * tax_rate
    
    # Shipping (free over $50, otherwise $5)
    shipping = Decimal('0.00') if subtotal >= 50 else Decimal('5.00')
    
    total = subtotal + tax + shipping - discount_amount
    
    # Process payment using mocked payment service
    try:
        payment_result = process_payment_mock(data['payment'], total)
    except Exception as e:
        return jsonify({
            'error': f'Payment processing error: {str(e)}',
            'error_code': 'PAYMENT_ERROR'
        }), 500
    
    if not payment_result.get('success'):
        return jsonify({
            'error': payment_result.get('error', 'Payment processing failed'),
            'error_code': payment_result.get('error_code', 'PAYMENT_FAILED')
        }), 400
    
    # Create order
    order = Order(
        order_number=Order.generate_order_number(),
        user_id=user_id,
        subtotal=subtotal,
        tax=tax,
        shipping=shipping,
        discount_amount=discount_amount,
        discount_code_id=cart.discount_code_id if cart.discount_code else None,
        discount_code=cart.discount_code.code if cart.discount_code else None,
        total=total,
        status=Order.STATUS_CONFIRMED,
        payment_status='paid',
        transaction_id=payment_result['transaction_id'],
        payment_method='credit_card',
        shipping_address=data['shipping_address'],
        confirmed_at=datetime.utcnow()
    )
    db.session.add(order)
    
    # Create order items and update stock
    for cart_item in cart.items:
        # Check stock again before creating order
        if cart_item.quantity > cart_item.product.stock:
            db.session.rollback()
            return jsonify({
                'error': f'Insufficient stock for {cart_item.product.title}'
            }), 400
        
        # Create order item
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            product_title=cart_item.product.title,
            product_price=cart_item.product.price,
            product_sku=cart_item.product.sku,
            quantity=cart_item.quantity,
            subtotal=cart_item.subtotal
        )
        db.session.add(order_item)
        
        # Update product stock
        cart_item.product.stock -= cart_item.quantity
        if cart_item.product.stock <= 0:
            cart_item.product.in_stock = False
    
    # Update discount code usage
    if cart.discount_code:
        cart.discount_code.used_count += 1
    
    # Clear cart
    CartItem.query.filter_by(cart_id=cart.id).delete()
    cart.discount_code_id = None
    
    db.session.commit()
    
    # Send email notification (mock)
    # In production, use celery task for async email sending
    try:
        from app.services.email_service import send_order_confirmation_email
        send_order_confirmation_email(order, user_id)
    except ImportError:
        # Email service not implemented - this is expected in development
        print(f"[MOCK EMAIL] Order confirmation email would be sent for order {order.order_number}")
    except Exception as e:
        # Don't fail order if email fails
        print(f"[WARNING] Email sending failed: {str(e)}")
    
    return jsonify({
        'order': order_schema.dump(order),
        'transaction_id': payment_result['transaction_id'],
        'message': 'Payment processed successfully using mocked payment service'
    }), 200
