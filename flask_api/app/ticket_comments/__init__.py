from flask import Blueprint

ticket_comments_bp = Blueprint('ticket_comments', __name__)

from app.ticket_comments import routes
