from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.users import users_bp
from app.models.user import User
from app.schemas.user import UserSchema, UserUpdateSchema, UserAdminUpdateSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_update_schema = UserUpdateSchema()
user_admin_update_schema = UserAdminUpdateSchema()

@users_bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    """
    Get all users
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: per_page
        type: integer
        default: 20
    responses:
      200:
        description: List of users
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)  # Max 100 per page
    
    users = User.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'users': users_schema.dump(users.items),
        'total': users.total,
        'pages': users.pages,
        'current_page': page
    }), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    Get user by ID
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
    responses:
      200:
        description: User information
      404:
        description: User not found
    """
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user)), 200

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    Update user
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            email:
              type: string
            first_name:
              type: string
            last_name:
              type: string
            password:
              type: string
    responses:
      200:
        description: User updated successfully
      403:
        description: Forbidden
      404:
        description: User not found
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    user = User.query.get_or_404(user_id)
    
    # Users can only update their own profile, admins can update any user
    is_own_profile = current_user_id == user_id
    is_admin = current_user.is_admin_user()
    
    if not is_own_profile and not is_admin:
        return jsonify({
            'status': 'error',
            'message': 'Access denied. You can only update your own profile.',
            'code': 'FORBIDDEN'
        }), 403
    
    # Check if request includes role or is_active (admin-only fields)
    request_data = request.json or {}
    has_role_update = 'role' in request_data
    has_active_update = 'is_active' in request_data
    
    # Non-admin users cannot update role or is_active
    if not is_admin and (has_role_update or has_active_update):
        return jsonify({
            'status': 'error',
            'message': 'Access denied. Only administrators can update user role or active status.',
            'code': 'FORBIDDEN'
        }), 403
    
    # Use admin schema if admin, regular schema otherwise
    try:
        if is_admin:
            data = user_admin_update_schema.load(request.json, partial=True)
        else:
            # Remove role and is_active from data for non-admin updates
            update_data = {k: v for k, v in (request.json or {}).items() 
                          if k not in ['role', 'is_active']}
            data = user_update_schema.load(update_data, partial=True)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Validation failed',
            'code': 'VALIDATION_ERROR',
            'errors': str(e)
        }), 400
    
    # Update fields
    if 'email' in data:
        # Check if email is already in use by another user
        existing_user = User.query.filter(
            User.email == data['email'],
            User.id != user_id
        ).first()
        if existing_user:
            return jsonify({
                'status': 'error',
                'message': 'Email already in use',
                'code': 'VALIDATION_ERROR'
            }), 400
        user.email = data['email']
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'name' in data:
        user.name = data['name']
    if 'password' in data:
        user.set_password(data['password'])
    if 'availability_status' in data:
        user.availability_status = data['availability_status']
    if 'expertise_areas' in data:
        user.expertise_areas = data['expertise_areas']
    
    # Admin-only fields
    if is_admin:
        if 'role' in data:
            # Prevent admins from removing their own admin role
            if user_id == current_user_id and data['role'] != User.ROLE_ADMIN:
                return jsonify({
                    'status': 'error',
                    'message': 'You cannot remove your own admin role',
                    'code': 'VALIDATION_ERROR'
                }), 400
            user.role = data['role']
            # Sync is_admin flag with role
            if data['role'] == User.ROLE_ADMIN:
                user.is_admin = True
            elif data['role'] != User.ROLE_ADMIN and user_id != current_user_id:
                # Allow removing admin flag only if not self
                user.is_admin = False
        
        if 'is_active' in data:
            # Prevent admins from deactivating themselves
            if user_id == current_user_id and not data['is_active']:
                return jsonify({
                    'status': 'error',
                    'message': 'You cannot deactivate your own account',
                    'code': 'VALIDATION_ERROR'
                }), 400
            user.is_active = data['is_active']
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to update user: {str(e)}',
            'code': 'DATABASE_ERROR'
        }), 400
    
    return jsonify(user_schema.dump(user)), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """
    Delete user
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
    responses:
      204:
        description: User deleted successfully
      403:
        description: Forbidden
      404:
        description: User not found
    """
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    current_user = User.query.get(current_user_id)
    
    if user_id != current_user_id and not current_user.is_admin:
        return jsonify({'error': 'Forbidden'}), 403
    
    db.session.delete(user)
    db.session.commit()
    
    return '', 204
