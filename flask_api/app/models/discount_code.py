"""Discount code model for e-commerce"""
from datetime import datetime
from app import db
from decimal import Decimal


class DiscountCode(db.Model):
    """Discount code model"""
    __tablename__ = 'discount_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Discount type: 'percentage' or 'fixed'
    discount_type = db.Column(db.String(20), nullable=False, default='percentage')
    
    # Discount value
    discount_percent = db.Column(db.Numeric(5, 2), nullable=True)  # For percentage (e.g., 10.00 for 10%)
    discount_amount = db.Column(db.Numeric(10, 2), nullable=True)  # For fixed amount
    
    # Constraints
    min_purchase = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    max_discount = db.Column(db.Numeric(10, 2), nullable=True)  # Maximum discount for percentage codes
    
    # Validity
    expires_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Usage limits
    usage_limit = db.Column(db.Integer, nullable=True)  # Total usage limit
    used_count = db.Column(db.Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def is_valid(self):
        """Check if discount code is valid"""
        if not self.is_active:
            return False
        
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False
        
        return True
    
    def calculate_discount(self, amount):
        """Calculate discount amount for given cart total"""
        if not self.is_valid():
            return Decimal('0.00')
        
        if amount < self.min_purchase:
            return Decimal('0.00')
        
        if self.discount_type == 'percentage':
            discount = amount * (self.discount_percent / 100)
            if self.max_discount:
                discount = min(discount, self.max_discount)
        elif self.discount_type == 'fixed':
            discount = self.discount_amount
        else:
            discount = Decimal('0.00')
        
        # Ensure discount doesn't exceed amount
        return min(discount, amount)
    
    def to_dict(self):
        """Convert discount code to dictionary"""
        return {
            'id': self.id,
            'code': self.code,
            'discount_type': self.discount_type,
            'discount_percent': float(self.discount_percent) if self.discount_percent else None,
            'discount_amount': float(self.discount_amount) if self.discount_amount else None,
            'min_purchase': float(self.min_purchase),
            'max_discount': float(self.max_discount) if self.max_discount else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active,
            'usage_limit': self.usage_limit,
            'used_count': self.used_count,
            'is_valid': self.is_valid()
        }
    
    def __repr__(self):
        return f'<DiscountCode {self.code}>'
