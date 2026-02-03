"""Order routes"""
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.orders import orders_bp
from app import db
from app.models import Order
from app.schemas.order import OrderSchema
from sqlalchemy import desc


order_schema = OrderSchema()


@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    """Get user's orders"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)  # Max 100 per page
    
    orders = Order.query.filter_by(user_id=user_id)\
        .order_by(desc(Order.created_at))\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'orders': [order_schema.dump(order) for order in orders.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': orders.total,
            'pages': orders.pages
        }
    }), 200


@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get order details"""
    user_id = get_jwt_identity()
    
    order = Order.query.get_or_404(order_id)
    
    # Check if user owns the order
    if order.user_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403
    
    return jsonify({'order': order_schema.dump(order)}), 200
