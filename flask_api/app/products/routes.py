"""Products routes"""
from flask import jsonify, request
from app.products import products_bp
from app import db
from app.models import Product
from app.schemas.product import ProductSchema
from sqlalchemy import or_


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@products_bp.route('', methods=['GET'])
def get_products():
    """Get all products"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)
    
    category = request.args.get('category', type=str)
    search = request.args.get('search', type=str)
    in_stock_only = request.args.get('in_stock_only', 'false', type=str).lower() == 'true'
    
    query = Product.query
    
    # Filter by category
    if category:
        query = query.filter(Product.category == category)
    
    # Search
    if search:
        search_pattern = f'%{search}%'
        query = query.filter(
            or_(
                Product.title.ilike(search_pattern),
                Product.description.ilike(search_pattern)
            )
        )
    
    # Filter by stock
    if in_stock_only:
        query = query.filter(Product.in_stock == True, Product.stock > 0)
    
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'products': [product.to_dict() for product in products.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': products.total,
            'pages': products.pages
        }
    }), 200


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get product by ID"""
    product = Product.query.get_or_404(product_id)
    return jsonify({'product': product.to_dict()}), 200
