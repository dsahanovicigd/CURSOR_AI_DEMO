from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from app.auth import auth_bp
from app.models.user import User
from app.schemas.user import UserCreateSchema, UserLoginSchema, UserSchema

user_schema = UserSchema()
user_create_schema = UserCreateSchema()
user_login_schema = UserLoginSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
              example: johndoe
            email:
              type: string
              example: john@example.com
            password:
              type: string
              example: securepassword123
            first_name:
              type: string
              example: John
            last_name:
              type: string
              example: Doe
    responses:
      201:
        description: User created successfully
      400:
        description: Validation error
    """
    try:
        data = user_create_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        name=data.get('name'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        role=data.get('role', User.ROLE_CUSTOMER),
        availability_status=data.get('availability_status'),
        expertise_areas=data.get('expertise_areas')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user_schema.dump(user)), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and get JWT tokens
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: johndoe
            password:
              type: string
              example: securepassword123
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    try:
        data = user_login_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']) and user.is_active:
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user_schema.dump(user)
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: Token refreshed successfully
    """
    current_user_id = get_jwt_identity()
    new_token = create_access_token(identity=current_user_id)
    
    return jsonify({'access_token': new_token}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: Current user information
    """
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    
    return jsonify(user_schema.dump(user)), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user (clear token on client side)
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: Logout successful
        schema:
          type: object
          properties:
            message:
              type: string
              example: Successfully logged out. Please clear your token in Swagger UI.
    """
    # Note: JWT tokens are stateless, so we can't truly "revoke" them server-side
    # This endpoint is mainly for client-side cleanup and consistency
    # In production, you might want to implement token blacklisting
    return jsonify({
        'message': 'Successfully logged out. Please clear your authorization in Swagger UI by clicking "Authorize" → "Logout".'
    }), 200
