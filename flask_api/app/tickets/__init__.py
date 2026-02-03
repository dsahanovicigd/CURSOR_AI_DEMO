from flask import Blueprint

tickets_bp = Blueprint('tickets', __name__)

from app.tickets import routes
from app.tickets import attachments  # Import attachment routes
