from marshmallow import Schema, fields, validate, validates, ValidationError

class CommentSchema(Schema):
    """Comment serialization schema"""
    id = fields.Integer(dump_only=True)
    content = fields.String(required=True, validate=validate.Length(min=1, max=5000))
    post_id = fields.Integer(required=True)
    user_id = fields.Integer(dump_only=True)
    author = fields.String(dump_only=True)
    author_name = fields.String(dump_only=True)
    parent_id = fields.Integer(allow_none=True)
    is_approved = fields.Boolean(dump_only=True)
    reply_count = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    class Meta:
        ordered = True

class CommentCreateSchema(Schema):
    """Comment creation schema"""
    content = fields.String(required=True, validate=validate.Length(min=1, max=5000))
    post_id = fields.Integer(required=True)
    parent_id = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    
    @validates('content')
    def validate_content(self, value):
        """Validate comment content"""
        if not value or not value.strip():
            raise ValidationError('Comment content cannot be empty')
        if len(value) > 5000:
            raise ValidationError('Comment content must be 5000 characters or less')
    
    class Meta:
        ordered = True

class CommentUpdateSchema(Schema):
    """Comment update schema"""
    content = fields.String(validate=validate.Length(min=1, max=5000))
    is_approved = fields.Boolean()
    
    @validates('content')
    def validate_content(self, value):
        """Validate comment content"""
        if value and not value.strip():
            raise ValidationError('Comment content cannot be empty')
        if value and len(value) > 5000:
            raise ValidationError('Comment content must be 5000 characters or less')
    
    class Meta:
        ordered = True
