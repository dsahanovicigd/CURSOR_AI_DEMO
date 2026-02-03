from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from app import db
from app.categories import categories_bp
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
import re

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
category_create_schema = CategoryCreateSchema()
category_update_schema = CategoryUpdateSchema()

def generate_slug(name):
    """Generate URL-friendly slug from name"""
    slug = re.sub(r'[^\w\s-]', '', name.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:100]

@categories_bp.route('', methods=['GET'])
def get_categories():
    """
    Get all categories
    ---
    tags:
      - Categories
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: per_page
        type: integer
        default: 20
      - in: query
        name: search
        type: string
        description: Search categories by name
    responses:
      200:
        description: List of categories
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '', type=str).strip()
        per_page = min(per_page, 100)
        
        query = Category.query
        
        if search:
            query = query.filter(Category.name.ilike(f'%{search}%'))
        
        categories = query.order_by(Category.name.asc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'categories': categories_schema.dump(categories.items),
            'total': categories.total,
            'pages': categories.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve categories: {str(e)}'}), 500

@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Get category by ID
    ---
    tags:
      - Categories
    parameters:
      - in: path
        name: category_id
        type: integer
        required: true
    responses:
      200:
        description: Category information
      404:
        description: Category not found
    """
    try:
        category = Category.query.get_or_404(category_id)
        return jsonify(category_schema.dump(category)), 200
    except Exception as e:
        if '404' in str(e):
            return jsonify({'error': 'Category not found'}), 404
        return jsonify({'error': f'Failed to retrieve category: {str(e)}'}), 500

@categories_bp.route('/slug/<slug>', methods=['GET'])
def get_category_by_slug(slug):
    """
    Get category by slug
    ---
    tags:
      - Categories
    parameters:
      - in: path
        name: slug
        type: string
        required: true
    responses:
      200:
        description: Category information
      404:
        description: Category not found
    """
    try:
        category = Category.query.filter_by(slug=slug).first_or_404()
        return jsonify(category_schema.dump(category)), 200
    except Exception as e:
        if '404' in str(e):
            return jsonify({'error': 'Category not found'}), 404
        return jsonify({'error': f'Failed to retrieve category: {str(e)}'}), 500

@categories_bp.route('', methods=['POST'])
@jwt_required()
def create_category():
    """
    Create a new category
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              example: Technology
            description:
              type: string
              example: Posts about technology and innovation
    responses:
      201:
        description: Category created successfully
      400:
        description: Validation error
      401:
        description: Unauthorized
      403:
        description: Forbidden - Admin only
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin_user():
            return jsonify({'error': 'Forbidden: Admin access required'}), 403
        
        data = category_create_schema.load(request.json)
        
        # Check if category with same name already exists
        existing_category = Category.query.filter_by(name=data['name']).first()
        if existing_category:
            return jsonify({'error': 'Category with this name already exists'}), 400
        
        slug = generate_slug(data['name'])
        
        # Ensure slug is unique
        counter = 1
        base_slug = slug
        while Category.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        category = Category(
            name=data['name'],
            slug=slug,
            description=data.get('description')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify(category_schema.dump(category)), 201
    except Exception as e:
        db.session.rollback()
        if hasattr(e, 'messages'):
            return jsonify({'error': 'Validation error', 'messages': e.messages}), 400
        return jsonify({'error': f'Failed to create category: {str(e)}'}), 400

@categories_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    """
    Update category
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    parameters:
      - in: path
        name: category_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
    responses:
      200:
        description: Category updated successfully
      400:
        description: Validation error
      403:
        description: Forbidden - Admin only
      404:
        description: Category not found
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin_user():
            return jsonify({'error': 'Forbidden: Admin access required'}), 403
        
        category = Category.query.get_or_404(category_id)
        data = category_update_schema.load(request.json, partial=True)
        
        # If name is being updated, check for duplicates and update slug
        if 'name' in data:
            existing_category = Category.query.filter(
                Category.name == data['name'],
                Category.id != category_id
            ).first()
            if existing_category:
                return jsonify({'error': 'Category with this name already exists'}), 400
            
            slug = generate_slug(data['name'])
            # Ensure slug is unique
            counter = 1
            base_slug = slug
            while Category.query.filter(Category.slug == slug, Category.id != category_id).first():
                slug = f"{base_slug}-{counter}"
                counter += 1
            data['slug'] = slug
        
        for key, value in data.items():
            setattr(category, key, value)
        
        db.session.commit()
        
        return jsonify(category_schema.dump(category)), 200
    except Exception as e:
        db.session.rollback()
        if '404' in str(e):
            return jsonify({'error': 'Category not found'}), 404
        if hasattr(e, 'messages'):
            return jsonify({'error': 'Validation error', 'messages': e.messages}), 400
        return jsonify({'error': f'Failed to update category: {str(e)}'}), 400

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    """
    Delete category
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    parameters:
      - in: path
        name: category_id
        type: integer
        required: true
    responses:
      204:
        description: Category deleted successfully
      403:
        description: Forbidden - Admin only
      404:
        description: Category not found
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin_user():
            return jsonify({'error': 'Forbidden: Admin access required'}), 403
        
        category = Category.query.get_or_404(category_id)
        
        db.session.delete(category)
        db.session.commit()
        
        return '', 204
    except Exception as e:
        db.session.rollback()
        if '404' in str(e):
            return jsonify({'error': 'Category not found'}), 404
        return jsonify({'error': f'Failed to delete category: {str(e)}'}), 500
