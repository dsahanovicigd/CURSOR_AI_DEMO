from flask import Blueprint

task_comments_bp = Blueprint('task_comments', __name__)

from app.task_comments import routes
