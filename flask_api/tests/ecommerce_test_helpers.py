"""
E-Commerce Test Helper Utilities

This module provides helper functions and mock data generators
for e-commerce checkout process tests.
"""

from faker import Faker
from decimal import Decimal
from datetime import datetime, timedelta
import random

fake = Faker()


class EcommerceMockDataGenerator:
    """Generate mock data for e-commerce testing"""
    
    @staticmethod
    def generate_product_data(**overrides):
        """Generate mock product data
        
        Args:
            **overrides: Fields to override in generated data
            
        Returns:
            dict: Product data
        """
        default_data = {
            'id': random.randint(1, 1000),
            'name': fake.word().capitalize() + ' ' + fake.word().capitalize(),
            'price': Decimal(str(round(random.uniform(10.00, 200.00), 2))),
            'sku': f'PROD-{random.randint(1000, 9999)}',
            'stock': random.randint(0, 100),
            'description': fake.text(max_nb_chars=200),
            'category': fake.word(),
            'image_url': fake.image_url()
        }
        default_data.update(overrides)
        return default_data
    
    @staticmethod
    def generate_cart_item_data(product_id=None, quantity=None, **overrides):
        """Generate mock cart item data
        
        Args:
            product_id: Product ID (optional)
            quantity: Quantity (optional)
            **overrides: Fields to override
            
        Returns:
            dict: Cart item data
        """
        default_data = {
            'product_id': product_id or random.randint(1, 100),
            'quantity': quantity or random.randint(1, 5)
        }
        default_data.update(overrides)
        return default_data
    
    @staticmethod
    def generate_discount_code_data(**overrides):
        """Generate mock discount code data
        
        Args:
            **overrides: Fields to override
            
        Returns:
            dict: Discount code data
        """
        code_types = ['percentage', 'fixed']
        code_type = random.choice(code_types)
        
        default_data = {
            'code': fake.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'),
            'type': code_type,
            'discount_percent': random.randint(5, 50) if code_type == 'percentage' else None,
            'discount_amount': Decimal(str(random.randint(5, 50))) if code_type == 'fixed' else None,
            'min_purchase': Decimal(str(random.randint(0, 100))),
            'max_discount': Decimal(str(random.randint(10, 100))) if code_type == 'percentage' else None,
            'expires_at': datetime.utcnow() + timedelta(days=random.randint(1, 90)),
            'is_active': True,
            'usage_limit': random.randint(100, 1000) if random.choice([True, False]) else None,
            'used_count': 0
        }
        default_data.update(overrides)
        return default_data
    
    @staticmethod
    def generate_payment_data(**overrides):
        """Generate mock payment data
        
        Args:
            **overrides: Fields to override
            
        Returns:
            dict: Payment data
        """
        # Valid test card numbers (Luhn algorithm compliant)
        test_cards = [
            '4111111111111111',  # Visa test card
            '4242424242424242',  # Visa test card
            '5555555555554444',  # Mastercard test card
            '378282246310005'    # Amex test card
        ]
        
        expiry_year = datetime.now().year + random.randint(1, 5)
        
        default_data = {
            'card_number': random.choice(test_cards),
            'cardholder_name': fake.name(),
            'expiry_month': random.randint(1, 12),
            'expiry_year': expiry_year,
            'cvv': str(random.randint(100, 999)),
            'billing_address': {
                'street': fake.street_address(),
                'city': fake.city(),
                'state': fake.state_abbr(),
                'zip': fake.zipcode(),
                'country': 'US'
            }
        }
        default_data.update(overrides)
        return default_data
    
    @staticmethod
    def generate_shipping_address(**overrides):
        """Generate mock shipping address
        
        Args:
            **overrides: Fields to override
            
        Returns:
            dict: Shipping address data
        """
        default_data = {
            'full_name': fake.name(),
            'street': fake.street_address(),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'zip': fake.zipcode(),
            'country': 'US',
            'phone': fake.phone_number()
        }
        default_data.update(overrides)
        return default_data
    
    @staticmethod
    def generate_order_data(**overrides):
        """Generate mock order data
        
        Args:
            **overrides: Fields to override
            
        Returns:
            dict: Order data
        """
        default_data = {
            'order_number': f'ORD-{datetime.now().strftime("%Y%m%d")}-{random.randint(1000, 9999)}',
            'status': 'confirmed',
            'subtotal': Decimal(str(round(random.uniform(50.00, 500.00), 2))),
            'tax': Decimal(str(round(random.uniform(5.00, 50.00), 2))),
            'shipping': Decimal(str(round(random.uniform(5.00, 25.00), 2))),
            'discount': Decimal(str(round(random.uniform(0.00, 50.00), 2))),
            'total': Decimal(str(round(random.uniform(50.00, 500.00), 2))),
            'created_at': datetime.utcnow(),
            'items': []
        }
        default_data.update(overrides)
        return default_data
    
    @staticmethod
    def generate_invalid_payment_data():
        """Generate invalid payment data for negative testing
        
        Returns:
            list: List of invalid payment data dictionaries
        """
        return [
            # Invalid card number (fails Luhn check)
            {'card_number': '4111111111111112', 'expiry_month': 12, 'expiry_year': 2025, 'cvv': '123'},
            
            # Expired card
            {'card_number': '4111111111111111', 'expiry_month': 1, 'expiry_year': 2020, 'cvv': '123'},
            
            # Invalid CVV (too short)
            {'card_number': '4111111111111111', 'expiry_month': 12, 'expiry_year': 2025, 'cvv': '12'},
            
            # Invalid CVV (too long)
            {'card_number': '4111111111111111', 'expiry_month': 12, 'expiry_year': 2025, 'cvv': '1234'},
            
            # Invalid expiry month
            {'card_number': '4111111111111111', 'expiry_month': 13, 'expiry_year': 2025, 'cvv': '123'},
            
            # Invalid expiry month (zero)
            {'card_number': '4111111111111111', 'expiry_month': 0, 'expiry_year': 2025, 'cvv': '123'},
            
            # Missing required fields
            {'card_number': '4111111111111111'},  # Missing expiry and CVV
            {'expiry_month': 12, 'expiry_year': 2025},  # Missing card number
        ]
    
    @staticmethod
    def generate_security_test_data():
        """Generate security test data (SQL injection, XSS, etc.)
        
        Returns:
            dict: Security test data scenarios
        """
        return {
            'sql_injection_card_number': "4111111111111111' OR '1'='1",
            'sql_injection_name': "'; DROP TABLE orders; --",
            'xss_cardholder_name': '<script>alert("XSS")</script>',
            'xss_shipping_address': '<img src=x onerror=alert(1)>',
            'command_injection': '; rm -rf /',
            'path_traversal': '../../../etc/passwd',
            'null_byte': 'test\x00user',
            'oversized_field': 'A' * 10000
        }


class PaymentValidator:
    """Payment validation utilities"""
    
    @staticmethod
    def luhn_check(card_number):
        """Validate card number using Luhn algorithm
        
        Args:
            card_number: Card number as string
            
        Returns:
            bool: True if valid, False otherwise
        """
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10 == 0
    
    @staticmethod
    def validate_card_expiry(month, year):
        """Validate card expiry date
        
        Args:
            month: Expiry month (1-12)
            year: Expiry year
            
        Returns:
            bool: True if valid and not expired, False otherwise
        """
        if not (1 <= month <= 12):
            return False
        
        current_date = datetime.now()
        expiry_date = datetime(year, month, 1)
        return expiry_date > current_date
    
    @staticmethod
    def validate_cvv(cvv, card_type='visa'):
        """Validate CVV code
        
        Args:
            cvv: CVV code as string
            card_type: Card type (visa, mastercard, amex)
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not cvv or not cvv.isdigit():
            return False
        
        if card_type.lower() == 'amex':
            return len(cvv) == 4
        else:
            return len(cvv) == 3


class CartCalculator:
    """Cart calculation utilities"""
    
    @staticmethod
    def calculate_subtotal(items):
        """Calculate cart subtotal
        
        Args:
            items: List of cart items with price and quantity
            
        Returns:
            Decimal: Subtotal amount
        """
        subtotal = Decimal('0.00')
        for item in items:
            price = Decimal(str(item.get('price', 0)))
            quantity = int(item.get('quantity', 0))
            subtotal += price * quantity
        return subtotal
    
    @staticmethod
    def calculate_tax(subtotal, tax_rate=0.08):
        """Calculate tax amount
        
        Args:
            subtotal: Subtotal amount
            tax_rate: Tax rate (default 8%)
            
        Returns:
            Decimal: Tax amount
        """
        return Decimal(str(subtotal)) * Decimal(str(tax_rate))
    
    @staticmethod
    def calculate_discount(subtotal, discount_code):
        """Calculate discount amount
        
        Args:
            subtotal: Subtotal amount
            discount_code: Discount code dictionary
            
        Returns:
            Decimal: Discount amount
        """
        if discount_code.get('type') == 'percentage':
            discount = subtotal * (Decimal(str(discount_code.get('discount_percent', 0))) / 100)
            max_discount = discount_code.get('max_discount')
            if max_discount and discount > max_discount:
                discount = max_discount
        elif discount_code.get('type') == 'fixed':
            discount = Decimal(str(discount_code.get('discount_amount', 0)))
        else:
            discount = Decimal('0.00')
        
        # Ensure discount doesn't exceed subtotal
        return min(discount, subtotal)
    
    @staticmethod
    def calculate_total(subtotal, tax, shipping, discount):
        """Calculate final total
        
        Args:
            subtotal: Subtotal amount
            tax: Tax amount
            shipping: Shipping amount
            discount: Discount amount
            
        Returns:
            Decimal: Total amount
        """
        total = subtotal + tax + shipping - discount
        return max(total, Decimal('0.00'))  # Ensure total is not negative


class OrderNumberGenerator:
    """Order number generation utilities"""
    
    @staticmethod
    def generate_order_number(prefix='ORD'):
        """Generate unique order number
        
        Args:
            prefix: Order number prefix
            
        Returns:
            str: Order number
        """
        date_str = datetime.now().strftime('%Y%m%d')
        random_suffix = random.randint(1000, 9999)
        return f'{prefix}-{date_str}-{random_suffix}'
    
    @staticmethod
    def validate_order_number(order_number):
        """Validate order number format
        
        Args:
            order_number: Order number to validate
            
        Returns:
            bool: True if valid format, False otherwise
        """
        import re
        pattern = r'^[A-Z]{3}-\d{8}-\d{4}$'
        return bool(re.match(pattern, order_number))


# Example usage:
"""
from tests.ecommerce_test_helpers import (
    EcommerceMockDataGenerator,
    PaymentValidator,
    CartCalculator,
    OrderNumberGenerator
)

# Generate test data
product = EcommerceMockDataGenerator.generate_product_data(price=29.99)
cart_item = EcommerceMockDataGenerator.generate_cart_item_data(product_id=1, quantity=2)
discount = EcommerceMockDataGenerator.generate_discount_code_data(code='SAVE10', discount_percent=10)
payment = EcommerceMockDataGenerator.generate_payment_data()

# Validate payment
is_valid_card = PaymentValidator.luhn_check('4111111111111111')
is_valid_expiry = PaymentValidator.validate_card_expiry(12, 2025)

# Calculate cart totals
items = [{'price': 29.99, 'quantity': 2}]
subtotal = CartCalculator.calculate_subtotal(items)
tax = CartCalculator.calculate_tax(subtotal)
total = CartCalculator.calculate_total(subtotal, tax, Decimal('5.00'), Decimal('0.00'))

# Generate order number
order_number = OrderNumberGenerator.generate_order_number()
"""
