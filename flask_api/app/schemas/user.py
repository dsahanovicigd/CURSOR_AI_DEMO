from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.user import User

class UserSchema(Schema):
    """User serialization schema"""
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    name = fields.String(dump_only=True)
    first_name = fields.String(validate=validate.Length(max=100))
    last_name = fields.String(validate=validate.Length(max=100))
    role = fields.String(validate=validate.OneOf([
        User.ROLE_CUSTOMER,
        User.ROLE_AGENT,
        User.ROLE_ADMIN
    ]))
    is_active = fields.Boolean(dump_only=True)
    is_admin = fields.Boolean(dump_only=True)
    availability_status = fields.String(validate=validate.OneOf([
        User.AVAILABILITY_AVAILABLE,
        User.AVAILABILITY_BUSY,
        User.AVAILABILITY_OFFLINE
    ]), allow_none=True)
    expertise_areas = fields.List(fields.String(), allow_none=True)
    open_ticket_count = fields.Integer(dump_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    class Meta:
        ordered = True

class UserCreateSchema(Schema):
    """User creation schema"""
    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8), load_only=True)
    name = fields.String(validate=validate.Length(max=200))
    first_name = fields.String(validate=validate.Length(max=100))
    last_name = fields.String(validate=validate.Length(max=100))
    role = fields.String(load_default=User.ROLE_CUSTOMER, validate=validate.OneOf([
        User.ROLE_CUSTOMER,
        User.ROLE_AGENT,
        User.ROLE_ADMIN
    ]))
    availability_status = fields.String(validate=validate.OneOf([
        User.AVAILABILITY_AVAILABLE,
        User.AVAILABILITY_BUSY,
        User.AVAILABILITY_OFFLINE
    ]), allow_none=True)
    expertise_areas = fields.List(fields.String(), allow_none=True)
    
    @validates('username')
    def validate_username(self, value):
        if User.query.filter_by(username=value).first():
            raise ValidationError('Username already exists')
    
    @validates('email')
    def validate_email(self, value):
        if User.query.filter_by(email=value).first():
            raise ValidationError('Email already exists')
    
    class Meta:
        ordered = True

class UserUpdateSchema(Schema):
    """User update schema - role can only be updated by admins"""
    email = fields.Email()
    name = fields.String(validate=validate.Length(max=200))
    first_name = fields.String(validate=validate.Length(max=100))
    last_name = fields.String(validate=validate.Length(max=100))
    password = fields.String(validate=validate.Length(min=8), load_only=True)
    role = fields.String(validate=validate.OneOf([
        User.ROLE_CUSTOMER,
        User.ROLE_AGENT,
        User.ROLE_ADMIN
    ]), allow_none=True)  # Role updates restricted in route handler
    availability_status = fields.String(validate=validate.OneOf([
        User.AVAILABILITY_AVAILABLE,
        User.AVAILABILITY_BUSY,
        User.AVAILABILITY_OFFLINE
    ]), allow_none=True)
    expertise_areas = fields.List(fields.String(), allow_none=True)
    
    class Meta:
        ordered = True

class UserAdminUpdateSchema(Schema):
    """Admin-only user update schema - allows role changes"""
    email = fields.Email()
    name = fields.String(validate=validate.Length(max=200))
    first_name = fields.String(validate=validate.Length(max=100))
    last_name = fields.String(validate=validate.Length(max=100))
    password = fields.String(validate=validate.Length(min=8), load_only=True)
    role = fields.String(validate=validate.OneOf([
        User.ROLE_CUSTOMER,
        User.ROLE_AGENT,
        User.ROLE_ADMIN
    ]))
    availability_status = fields.String(validate=validate.OneOf([
        User.AVAILABILITY_AVAILABLE,
        User.AVAILABILITY_BUSY,
        User.AVAILABILITY_OFFLINE
    ]), allow_none=True)
    expertise_areas = fields.List(fields.String(), allow_none=True)
    is_active = fields.Boolean()
    
    class Meta:
        ordered = True

class UserLoginSchema(Schema):
    """User login schema"""
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    
    class Meta:
        ordered = True
