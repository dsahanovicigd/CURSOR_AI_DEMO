from marshmallow import Schema, fields, validate, validates, ValidationError

class PostSchema(Schema):
    """Post serialization schema"""
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    slug = fields.String(dump_only=True)
    content = fields.String(required=True, validate=validate.Length(min=1))
    excerpt = fields.String(validate=validate.Length(max=500))
    user_id = fields.Integer(dump_only=True)
    author = fields.String(dump_only=True)
    author_name = fields.String(dump_only=True)
    is_published = fields.Boolean()
    view_count = fields.Integer(dump_only=True)
    tags = fields.List(fields.String(), dump_only=True)
    category_ids = fields.List(fields.Integer(), dump_only=True)
    category_names = fields.List(fields.String(), dump_only=True)
    comment_count = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    class Meta:
        ordered = True

class PostCreateSchema(Schema):
    """Post creation schema"""
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    content = fields.String(required=True, validate=validate.Length(min=1))
    excerpt = fields.String(validate=validate.Length(max=500))
    is_published = fields.Boolean(missing=True)
    tags = fields.List(fields.String(), validate=validate.Length(max=20))
    category_ids = fields.List(fields.Integer(), validate=validate.Length(max=10))
    
    @validates('title')
    def validate_title(self, value):
        """Validate post title"""
        if not value or not value.strip():
            raise ValidationError('Post title cannot be empty')
        if len(value) > 200:
            raise ValidationError('Post title must be 200 characters or less')
    
    @validates('content')
    def validate_content(self, value):
        """Validate post content"""
        if not value or not value.strip():
            raise ValidationError('Post content cannot be empty')
    
    @validates('tags')
    def validate_tags(self, value):
        """Validate tags"""
        if value:
            for tag in value:
                if len(tag) > 50:
                    raise ValidationError(f'Tag "{tag}" must be 50 characters or less')
                if not tag.strip():
                    raise ValidationError('Tags cannot be empty')
    
    class Meta:
        ordered = True

class PostUpdateSchema(Schema):
    """Post update schema"""
    title = fields.String(validate=validate.Length(min=1, max=200))
    content = fields.String(validate=validate.Length(min=1))
    excerpt = fields.String(validate=validate.Length(max=500))
    is_published = fields.Boolean()
    tags = fields.List(fields.String(), validate=validate.Length(max=20))
    category_ids = fields.List(fields.Integer(), validate=validate.Length(max=10))
    
    @validates('title')
    def validate_title(self, value):
        """Validate post title"""
        if value and not value.strip():
            raise ValidationError('Post title cannot be empty')
        if value and len(value) > 200:
            raise ValidationError('Post title must be 200 characters or less')
    
    @validates('content')
    def validate_content(self, value):
        """Validate post content"""
        if value and not value.strip():
            raise ValidationError('Post content cannot be empty')
    
    @validates('tags')
    def validate_tags(self, value):
        """Validate tags"""
        if value:
            for tag in value:
                if len(tag) > 50:
                    raise ValidationError(f'Tag "{tag}" must be 50 characters or less')
                if not tag.strip():
                    raise ValidationError('Tags cannot be empty')
    
    class Meta:
        ordered = True
