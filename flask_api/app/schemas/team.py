from marshmallow import Schema, fields, validate

class TeamSchema(Schema):
    """Team serialization schema"""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(validate=validate.Length(max=5000))
    owner_id = fields.Integer(dump_only=True)
    owner_name = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    member_count = fields.Integer(dump_only=True)
    project_count = fields.Integer(dump_only=True)
    
    class Meta:
        ordered = True

class TeamCreateSchema(Schema):
    """Team creation schema"""
    name = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(validate=validate.Length(max=5000))
    
    class Meta:
        ordered = True

class TeamUpdateSchema(Schema):
    """Team update schema"""
    name = fields.String(validate=validate.Length(min=1, max=200))
    description = fields.String(validate=validate.Length(max=5000))
    
    class Meta:
        ordered = True

class TeamMemberSchema(Schema):
    """Team member schema"""
    user_id = fields.Integer(required=True)
    role = fields.String(validate=validate.OneOf(['owner', 'admin', 'member']), missing='member')
    
    class Meta:
        ordered = True
