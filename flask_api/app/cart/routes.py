"""Cart routes"""
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.cart import cart_bp
from app import db
from app.models import Cart, CartItem, Product, DiscountCode
from app.schemas.cart import CartSchema, AddToCartSchema, UpdateCartItemSchema, ApplyDiscountSchema
from marshmallow import ValidationError
from datetime import datetime


cart_schema = CartSchema()
add_to_cart_schema = AddToCartSchema()
update_cart_item_schema = UpdateCartItemSchema()
apply_discount_schema = ApplyDiscountSchema()


def get_or_create_cart(user_id):
    """Get or create cart for user"""
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    return cart


@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    """Get user's cart"""
    user_id = get_jwt_identity()
    cart = get_or_create_cart(user_id)
    # Use to_dict() to ensure all calculated fields are included
    return jsonify({'cart': cart.to_dict()}), 200


@cart_bp.route('/items', methods=['POST'])
@jwt_required()
def add_to_cart():
    """Add item to cart"""
    try:
        data = add_to_cart_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'messages': err.messages}), 400
    
    user_id = get_jwt_identity()
    cart = get_or_create_cart(user_id)
    
    # Check if product exists
    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Check stock
    if not product.in_stock or product.stock <= 0:
        return jsonify({'error': 'Product is out of stock'}), 400
    
    if data['quantity'] > product.stock:
        return jsonify({'error': f'Insufficient stock. Available: {product.stock}'}), 400
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
    
    if cart_item:
        # Update quantity
        new_quantity = cart_item.quantity + data['quantity']
        if new_quantity > product.stock:
            return jsonify({'error': f'Insufficient stock. Available: {product.stock}'}), 400
        cart_item.quantity = new_quantity
    else:
        # Create new cart item
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=data['quantity']
        )
        db.session.add(cart_item)
    
    db.session.commit()
    
    # Refresh cart
    db.session.refresh(cart)
    return jsonify({'cart': cart.to_dict()}), 200


@cart_bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    """Update cart item quantity"""
    try:
        data = update_cart_item_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'messages': err.messages}), 400
    
    user_id = get_jwt_identity()
    cart = get_or_create_cart(user_id)
    
    cart_item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404
    
    if data['quantity'] == 0:
        # Remove item
        db.session.delete(cart_item)
        db.session.commit()
        db.session.refresh(cart)
        return jsonify({'cart': cart_schema.dump(cart)}), 200
    
    # Check stock
    if data['quantity'] > cart_item.product.stock:
        return jsonify({'error': f'Insufficient stock. Available: {cart_item.product.stock}'}), 400
    
    cart_item.quantity = data['quantity']
    db.session.commit()
    
    db.session.refresh(cart)
    return jsonify({'cart': cart.to_dict()}), 200


@cart_bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_cart_item(item_id):
    """Remove item from cart"""
    user_id = get_jwt_identity()
    cart = get_or_create_cart(user_id)
    
    cart_item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404
    
    db.session.delete(cart_item)
    db.session.commit()
    
    db.session.refresh(cart)
    return jsonify({'cart': cart.to_dict()}), 200


@cart_bp.route('', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """Clear all items from cart"""
    user_id = get_jwt_identity()
    cart = get_or_create_cart(user_id)
    
    CartItem.query.filter_by(cart_id=cart.id).delete()
    cart.discount_code_id = None
    db.session.commit()
    
    db.session.refresh(cart)
    return jsonify({'cart': cart.to_dict()}), 200


@cart_bp.route('/apply-discount', methods=['POST'])
@jwt_required()
def apply_discount():
    """Apply discount code to cart"""
    try:
        data = apply_discount_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'messages': err.messages}), 400
    
    user_id = get_jwt_identity()
    cart = get_or_create_cart(user_id)
    
    # Check if cart is empty
    if cart.items.count() == 0:
        return jsonify({'error': 'Cart is empty'}), 400
    
    # Find discount code
    discount_code = DiscountCode.query.filter_by(code=data['discount_code']).first()
    if not discount_code:
        return jsonify({'error': 'Invalid discount code'}), 400
    
    # Validate discount code
    if not discount_code.is_valid():
        # Check expiry using datetime comparison (not db.func.now() which doesn't work in Python)
        if discount_code.expires_at and discount_code.expires_at < datetime.utcnow():
            return jsonify({'error': 'Discount code has expired'}), 400
        if discount_code.usage_limit and discount_code.used_count >= discount_code.usage_limit:
            return jsonify({'error': 'Discount code usage limit reached'}), 400
        return jsonify({'error': 'Discount code is not active'}), 400
    
    # Check minimum purchase
    subtotal = cart.calculate_subtotal()
    if subtotal < discount_code.min_purchase:
        return jsonify({
            'error': f'Minimum purchase of ${discount_code.min_purchase} required'
        }), 400
    
    # Apply discount
    cart.discount_code_id = discount_code.id
    db.session.commit()
    
    db.session.refresh(cart)
    return jsonify({'cart': cart.to_dict()}), 200


@cart_bp.route('/discount', methods=['DELETE'])
@jwt_required()
def remove_discount():
    """Remove discount code from cart"""
    user_id = get_jwt_identity()
    cart = get_or_create_cart(user_id)
    
    cart.discount_code_id = None
    db.session.commit()
    
    db.session.refresh(cart)
    return jsonify({'cart': cart.to_dict()}), 200
