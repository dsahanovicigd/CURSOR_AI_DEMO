"""Checkout routes"""
from flask import Blueprint

checkout_bp = Blueprint('checkout', __name__, url_prefix='/api/checkout')

from app.checkout import routes
