"""Cart routes"""
from flask import Blueprint

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

from app.cart import routes
