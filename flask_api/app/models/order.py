"""Order models for e-commerce"""
from datetime import datetime
from app import db
from sqlalchemy import Index


class Order(db.Model):
    """Order model"""
    __tablename__ = 'orders'
    
    # Order statuses
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_PROCESSING = 'processing'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'
    STATUS_REFUNDED = 'refunded'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Order totals
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    tax = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    shipping = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    discount_amount = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Discount code
    discount_code_id = db.Column(db.Integer, db.ForeignKey('discount_codes.id'), nullable=True)
    discount_code = db.Column(db.String(50), nullable=True)  # Store code for reference
    
    # Payment
    payment_status = db.Column(db.String(20), default='pending', nullable=False)  # pending, paid, failed, refunded
    transaction_id = db.Column(db.String(100), nullable=True)
    payment_method = db.Column(db.String(50), default='credit_card', nullable=False)
    
    # Shipping address (stored as JSON)
    shipping_address = db.Column(db.JSON, nullable=False)
    
    # Order status
    status = db.Column(db.String(20), default=STATUS_PENDING, nullable=False, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    shipped_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='orders')
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan', order_by='OrderItem.id')
    
    @staticmethod
    def generate_order_number():
        """Generate unique order number"""
        from datetime import datetime
        import random
        date_str = datetime.utcnow().strftime('%Y%m%d')
        random_suffix = random.randint(1000, 9999)
        return f'ORD-{date_str}-{random_suffix}'
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items],
            'subtotal': float(self.subtotal),
            'tax': float(self.tax),
            'shipping': float(self.shipping),
            'discount_amount': float(self.discount_amount),
            'discount_code': self.discount_code,
            'total': float(self.total),
            'status': self.status,
            'payment_status': self.payment_status,
            'transaction_id': self.transaction_id,
            'payment_method': self.payment_method,
            'shipping_address': self.shipping_address,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None,
            'shipped_at': self.shipped_at.isoformat() if self.shipped_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None
        }
    
    def __repr__(self):
        return f'<Order {self.order_number}>'


class OrderItem(db.Model):
    """Order item model"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    
    # Store product details at time of order (in case product changes)
    product_title = db.Column(db.String(200), nullable=False)
    product_price = db.Column(db.Numeric(10, 2), nullable=False)
    product_sku = db.Column(db.String(100), nullable=True)
    
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert order item to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_title': self.product_title,
            'product_price': float(self.product_price),
            'product_sku': self.product_sku,
            'quantity': self.quantity,
            'subtotal': float(self.subtotal)
        }
    
    def __repr__(self):
        return f'<OrderItem {self.id}: {self.product_title} x{self.quantity}>'
