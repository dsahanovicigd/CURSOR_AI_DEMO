from flask import Flask, jsonify, request
from app.cache_utils import cached_search
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import Swagger
from app.cache import cache
from app.celery_app import make_celery

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()
# Use in-memory storage for development to reduce Redis activity
# For production, use Redis: storage_uri="redis://localhost:6379/1"
import os
limiter_storage = os.environ.get('LIMITER_STORAGE_URI', 'memory://')
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per minute"],
    storage_uri=limiter_storage
)
swagger = Swagger()  # Will be initialized in create_app

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize production-specific settings
    if hasattr(config[config_name], 'init_app'):
        config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    # CORS configuration - allow all origins in development
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600
        }
    })
    jwt.init_app(app)
    limiter.init_app(app)
    
    # Initialize caching
    try:
        cache.init_app(app)
    except Exception as e:
        # If Redis is unavailable, cache operations will fail silently
        # Cache decorators already handle exceptions gracefully
        app.logger.warning(f'Cache initialization warning (cache may be unavailable): {str(e)}')
    
    # Initialize Celery
    celery = make_celery(app)
    app.celery = celery
    
    # Swagger configuration
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/api/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs",
        "ui_params": {
            "deepLinking": True,
            "displayRequestDuration": True,
            "docExpansion": "list",
            "filter": True,
            "showExtensions": True,
            "showCommonExtensions": True,
            "tryItOutEnabled": True
        }
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Flask REST API - Blogging Platform",
            "description": "REST API for a blogging platform with SQLAlchemy, Marshmallow, JWT, and Swagger. Features include:\n- User authentication with JWT\n- Blog post CRUD operations\n- Comment system with nested replies\n- Category management\n- Search functionality\n- Tag support\n\n**To use protected endpoints:**\n1. Login at POST /api/auth/login to get an access_token\n2. Click the 'Authorize' button (🔒) at the top right\n3. Enter your token in the format: `Bearer <your_token>` (include 'Bearer' prefix)\n4. Click 'Authorize' and 'Close'\n5. Now all protected endpoints will automatically include your token!",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme.\n\n**How to use:**\n1. Login at POST /api/auth/login to get an access_token\n2. Click 'Authorize' button (🔒) at top right\n3. Enter your token in the format: `Bearer <your_access_token>`\n   - Include the word 'Bearer' followed by a space, then your token\n   - Example: `Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...`\n4. Click 'Authorize'\n\n**Note:** The token field requires the full format including 'Bearer' prefix."
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ]
    }
    
    # Initialize Swagger with custom config
    global swagger
    swagger = Swagger(app, config=swagger_config, template=swagger_template)
    
    # JWT Error Handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired. Please refresh your token.'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': f'Invalid token. {str(error)}'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'error': 'Authorization header is missing or invalid.',
            'message': 'Please include a valid JWT token in the Authorization header.',
            'format': 'Authorization: Bearer <your_access_token>',
            'hint': 'First, login at POST /api/auth/login to get an access_token'
        }), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Fresh token required. Please refresh your token.'}), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has been revoked.'}), 401
    
    # Register blueprints
    from app.auth import auth_bp
    from app.users import users_bp
    from app.posts import posts_bp
    from app.categories import categories_bp
    from app.comments import comments_bp
    from app.tasks import tasks_bp
    from app.projects import projects_bp
    from app.teams import teams_bp
    from app.notifications import notifications_bp
    from app.task_comments import task_comments_bp
    from app.tickets import tickets_bp
    from app.ticket_comments import ticket_comments_bp
    from app.admin import admin_bp
    from app.agents import agents_bp
    from app.cart import cart_bp
    from app.checkout import checkout_bp
    from app.orders import orders_bp
    from app.products import products_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(posts_bp, url_prefix='/api/posts')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(comments_bp, url_prefix='/api/comments')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(teams_bp, url_prefix='/api/teams')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    app.register_blueprint(task_comments_bp, url_prefix='/api')
    app.register_blueprint(tickets_bp, url_prefix='/api/tickets')
    app.register_blueprint(ticket_comments_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(agents_bp, url_prefix='/api/agents')
    app.register_blueprint(cart_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(products_bp)
    
    # Register cache monitoring blueprint (if available)
    try:
        from app.cache_monitoring import cache_monitoring_bp
        app.register_blueprint(cache_monitoring_bp, url_prefix='/api/cache')
    except ImportError:
        pass
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'API is running'}, 200
    
    # General search endpoint
    @app.route('/api/search', methods=['GET'])
    @cached_search(timeout=300)
    def search():
        """
        General search endpoint
        ---
        tags:
          - Search
        parameters:
          - in: query
            name: q
            type: string
            required: true
            description: Search query
          - in: query
            name: page
            type: integer
            default: 1
          - in: query
            name: per_page
            type: integer
            default: 20
          - in: query
            name: category_id
            type: integer
            description: Filter by category
          - in: query
            name: tag
            type: string
            description: Filter by tag
        responses:
          200:
            description: Search results
          400:
            description: Invalid search query
        """
        from app.models.post import Post
        from app.models.category import Category
        from sqlalchemy import or_
        
        search_query = request.args.get('q', '', type=str).strip()
        if not search_query:
            return jsonify({'error': 'Search query is required'}), 400
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category_id = request.args.get('category_id', type=int)
        tag = request.args.get('tag', '', type=str).strip()
        per_page = min(per_page, 100)
        
        query = Post.query.filter_by(is_published=True)
        
        # Search in title, content, and excerpt
        search_pattern = f'%{search_query}%'
        query = query.filter(
            or_(
                Post.title.ilike(search_pattern),
                Post.content.ilike(search_pattern),
                Post.excerpt.ilike(search_pattern)
            )
        )
        
        # Filter by category
        if category_id:
            category = Category.query.get(category_id)
            if category:
                query = query.filter(Post.categories.contains(category))
        
        # Filter by tag
        if tag:
            query = query.filter(Post.tags.ilike(f'%{tag}%'))
        
        posts = query.order_by(Post.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'query': search_query,
            'posts': [post.to_dict() for post in posts.items],
            'total': posts.total,
            'pages': posts.pages,
            'current_page': page
        }), 200
    
    return app
