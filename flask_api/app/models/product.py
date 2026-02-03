"""Product model for e-commerce"""
from datetime import datetime
from app import db
from sqlalchemy import JSON


class Product(db.Model):
    """Product model for e-commerce catalog"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    original_price = db.Column(db.Numeric(10, 2), nullable=True)
    currency = db.Column(db.String(10), default='USD', nullable=False)
    image = db.Column(db.String(500), nullable=True)
    
    # Stock management
    stock = db.Column(db.Integer, default=0, nullable=False)
    in_stock = db.Column(db.Boolean, default=True, nullable=False)
    
    # Product details
    category = db.Column(db.String(100), nullable=True, index=True)
    sku = db.Column(db.String(100), unique=True, nullable=True, index=True)
    colors = db.Column(JSON, nullable=True)  # Array of color hex codes
    sizes = db.Column(JSON, nullable=True)   # Array of sizes
    
    # Ratings
    rating_average = db.Column(db.Numeric(3, 2), default=0.0, nullable=False)
    rating_count = db.Column(db.Integer, default=0, nullable=False)
    
    # Badge
    badge_type = db.Column(db.String(50), nullable=True)  # sale, new, trending, limited, bestseller
    badge_text = db.Column(db.String(100), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    cart_items = db.relationship('CartItem', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    
    def to_dict(self):
        """Convert product to dictionary"""
        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'price': float(self.price),
            'originalPrice': float(self.original_price) if self.original_price else None,
            'currency': self.currency,
            'image': self.image,
            'rating': {
                'average': float(self.rating_average),
                'count': self.rating_count
            },
            'category': self.category,
            'inStock': self.in_stock and self.stock > 0,
            'stock': self.stock,
            'badge': {
                'text': self.badge_text,
                'type': self.badge_type
            } if self.badge_type else None,
            'colors': self.colors or [],
            'sizes': self.sizes or []
        }
    
    def __repr__(self):
        return f'<Product {self.id}: {self.title}>'
