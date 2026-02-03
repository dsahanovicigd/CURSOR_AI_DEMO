from marshmallow import Schema, fields, validate, validates, ValidationError
import re

class CategorySchema(Schema):
    """Category serialization schema"""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    slug = fields.String(dump_only=True)
    description = fields.String(validate=validate.Length(max=1000))
    post_count = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    class Meta:
        ordered = True

class CategoryCreateSchema(Schema):
    """Category creation schema"""
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String(validate=validate.Length(max=1000))
    
    @validates('name')
    def validate_name(self, value):
        """Validate category name"""
        if not value or not value.strip():
            raise ValidationError('Category name cannot be empty')
        if len(value) > 100:
            raise ValidationError('Category name must be 100 characters or less')
    
    class Meta:
        ordered = True

class CategoryUpdateSchema(Schema):
    """Category update schema"""
    name = fields.String(validate=validate.Length(min=1, max=100))
    description = fields.String(validate=validate.Length(max=1000))
    
    class Meta:
        ordered = True
