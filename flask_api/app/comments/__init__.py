from flask import Blueprint

comments_bp = Blueprint('comments', __name__)

from app.comments import routes
