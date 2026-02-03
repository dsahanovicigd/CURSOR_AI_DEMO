from marshmallow import Schema, fields, validate

class ProjectSchema(Schema):
    """Project serialization schema"""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(validate=validate.Length(max=5000))
    status = fields.String(validate=validate.OneOf(['active', 'archived', 'completed']))
    owner_id = fields.Integer(dump_only=True)
    owner_name = fields.String(dump_only=True)
    team_id = fields.Integer(allow_none=True)
    team_name = fields.String(dump_only=True)
    start_date = fields.DateTime(allow_none=True)
    end_date = fields.DateTime(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    member_count = fields.Integer(dump_only=True)
    task_count = fields.Integer(dump_only=True)
    
    class Meta:
        ordered = True

class ProjectCreateSchema(Schema):
    """Project creation schema"""
    name = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(validate=validate.Length(max=5000))
    status = fields.String(missing='active', validate=validate.OneOf(['active', 'archived', 'completed']))
    team_id = fields.Integer(allow_none=True)
    start_date = fields.DateTime(allow_none=True)
    end_date = fields.DateTime(allow_none=True)
    
    class Meta:
        ordered = True

class ProjectUpdateSchema(Schema):
    """Project update schema"""
    name = fields.String(validate=validate.Length(min=1, max=200))
    description = fields.String(validate=validate.Length(max=5000))
    status = fields.String(validate=validate.OneOf(['active', 'archived', 'completed']))
    team_id = fields.Integer(allow_none=True)
    start_date = fields.DateTime(allow_none=True)
    end_date = fields.DateTime(allow_none=True)
    
    class Meta:
        ordered = True

class ProjectMemberSchema(Schema):
    """Project member schema"""
    user_id = fields.Integer(required=True)
    role = fields.String(validate=validate.OneOf(['owner', 'admin', 'member']), missing='member')
    
    class Meta:
        ordered = True
