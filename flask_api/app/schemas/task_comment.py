from marshmallow import Schema, fields, validate

class TaskCommentSchema(Schema):
    """Task comment serialization schema"""
    id = fields.Integer(dump_only=True)
    content = fields.String(required=True, validate=validate.Length(min=1, max=5000))
    task_id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    user_name = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    class Meta:
        ordered = True

class TaskCommentCreateSchema(Schema):
    """Task comment creation schema"""
    content = fields.String(required=True, validate=validate.Length(min=1, max=5000))
    
    class Meta:
        ordered = True

class TaskCommentUpdateSchema(Schema):
    """Task comment update schema"""
    content = fields.String(required=True, validate=validate.Length(min=1, max=5000))
    
    class Meta:
        ordered = True
