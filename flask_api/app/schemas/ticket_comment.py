from marshmallow import Schema, fields, validate

class TicketCommentSchema(Schema):
    """Ticket comment serialization schema"""
    id = fields.Integer(dump_only=True)
    ticket_id = fields.Integer(dump_only=True)
    user_id = fields.Integer(allow_none=True)
    user_name = fields.String(dump_only=True)
    user_email = fields.String(dump_only=True)
    content = fields.String(required=True, validate=validate.Length(min=1, max=5000))
    is_internal = fields.Boolean(load_default=False)
    customer_email = fields.Email(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    attachment_count = fields.Integer(dump_only=True)
    
    class Meta:
        ordered = True

class TicketCommentCreateSchema(Schema):
    """Ticket comment creation schema"""
    content = fields.String(required=True, validate=validate.Length(min=1, max=5000))
    is_internal = fields.Boolean(load_default=False)
    customer_email = fields.Email(allow_none=True)  # For customer comments without account
    
    class Meta:
        ordered = True
