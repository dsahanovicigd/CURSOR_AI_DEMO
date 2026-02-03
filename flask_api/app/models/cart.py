"""Cart models for e-commerce"""
from datetime import datetime
from app import db
from sqlalchemy import UniqueConstraint
from decimal import Decimal


class Cart(db.Model):
    """Shopping cart model"""
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    
    # Discount code
    discount_code_id = db.Column(db.Integer, db.ForeignKey('discount_codes.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='cart', uselist=False)
    items = db.relationship('CartItem', backref='cart', lazy='dynamic', cascade='all, delete-orphan', order_by='CartItem.id')
    discount_code = db.relationship('DiscountCode', backref='carts')
    
    def calculate_subtotal(self):
        """Calculate cart subtotal"""
        return sum(item.subtotal for item in self.items)
    
    def calculate_total(self):
        """Calculate cart total with discount"""
        subtotal = self.calculate_subtotal()
        discount_amount = 0
        
        if self.discount_code and self.discount_code.is_active:
            discount_amount = self.discount_code.calculate_discount(subtotal)
        
        return max(subtotal - discount_amount, 0)
    
    def to_dict(self):
        """Convert cart to dictionary"""
        subtotal = self.calculate_subtotal()
        discount_amount = Decimal('0.00')
        if self.discount_code and self.discount_code.is_active:
            discount_amount = self.discount_code.calculate_discount(subtotal)
        
        items_list = [item.to_dict() for item in self.items]
        item_count = len(items_list)
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'items': items_list,
            'subtotal': float(subtotal),
            'discount_code': self.discount_code.code if self.discount_code else None,
            'discount_amount': float(discount_amount),
            'total': float(self.calculate_total()),
            'item_count': item_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Cart {self.id} for User {self.user_id}>'


class CartItem(db.Model):
    """Cart item model"""
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Unique constraint: one product per cart
    __table_args__ = (UniqueConstraint('cart_id', 'product_id', name='unique_cart_product'),)
    
    @property
    def subtotal(self):
        """Calculate item subtotal"""
        if self.product:
            return self.product.price * self.quantity
        return 0
    
    def to_dict(self):
        """Convert cart item to dictionary"""
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'product': self.product.to_dict() if self.product else None,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'subtotal': float(self.subtotal),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<CartItem {self.id}: Product {self.product_id} x{self.quantity}>'
