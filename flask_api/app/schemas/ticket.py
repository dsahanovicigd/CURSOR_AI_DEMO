from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.ticket import Ticket
import re

class TicketSchema(Schema):
    """Ticket serialization schema"""
    id = fields.Integer(dump_only=True)
    ticket_number = fields.String(dump_only=True)
    subject = fields.String(required=True, validate=validate.Length(min=5, max=200))
    description = fields.String(required=True, validate=validate.Length(min=20, max=5000))
    status = fields.String(validate=validate.OneOf([
        Ticket.STATUS_OPEN,
        Ticket.STATUS_ASSIGNED,
        Ticket.STATUS_IN_PROGRESS,
        Ticket.STATUS_WAITING,
        Ticket.STATUS_RESOLVED,
        Ticket.STATUS_CLOSED,
        Ticket.STATUS_REOPENED
    ]))
    priority = fields.String(validate=validate.OneOf([
        Ticket.PRIORITY_LOW,
        Ticket.PRIORITY_MEDIUM,
        Ticket.PRIORITY_HIGH,
        Ticket.PRIORITY_URGENT
    ]))
    category = fields.String(validate=validate.OneOf([
        Ticket.CATEGORY_TECHNICAL,
        Ticket.CATEGORY_BILLING,
        Ticket.CATEGORY_GENERAL,
        Ticket.CATEGORY_FEATURE_REQUEST
    ]))
    customer_email = fields.Email(required=True)
    assigned_to_id = fields.Integer(allow_none=True)
    assigned_to_name = fields.String(dump_only=True)
    created_by_id = fields.Integer(dump_only=True)
    created_by_name = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    resolved_at = fields.DateTime(dump_only=True)
    closed_at = fields.DateTime(dump_only=True)
    reopened_at = fields.DateTime(dump_only=True)
    first_response_at = fields.DateTime(dump_only=True)
    sla_response_deadline = fields.DateTime(dump_only=True)
    sla_resolution_deadline = fields.DateTime(dump_only=True)
    is_sla_breached = fields.Boolean(dump_only=True)
    comment_count = fields.Integer(dump_only=True)
    attachment_count = fields.Integer(dump_only=True)
    
    class Meta:
        ordered = True

class TicketCreateSchema(Schema):
    """Ticket creation schema"""
    subject = fields.String(required=True, validate=validate.Length(min=5, max=200))
    description = fields.String(required=True, validate=validate.Length(min=20, max=5000))
    priority = fields.String(missing=Ticket.PRIORITY_MEDIUM, validate=validate.OneOf([
        Ticket.PRIORITY_LOW,
        Ticket.PRIORITY_MEDIUM,
        Ticket.PRIORITY_HIGH,
        Ticket.PRIORITY_URGENT
    ]))
    category = fields.String(required=True, validate=validate.OneOf([
        Ticket.CATEGORY_TECHNICAL,
        Ticket.CATEGORY_BILLING,
        Ticket.CATEGORY_GENERAL,
        Ticket.CATEGORY_FEATURE_REQUEST
    ]))
    customer_email = fields.Email(required=True)
    
    @validates('subject')
    def validate_subject(self, value):
        """Validate subject contains only allowed characters"""
        if not re.match(r'^[a-zA-Z0-9\s\.,!?\-_()]+$', value):
            raise ValidationError('Subject contains invalid characters')
    
    @validates('description')
    def validate_description(self, value):
        """Validate description length and content"""
        if len(value.strip()) < 20:
            raise ValidationError('Description must be at least 20 characters')
    
    class Meta:
        ordered = True

class TicketUpdateSchema(Schema):
    """Ticket update schema"""
    subject = fields.String(validate=validate.Length(min=5, max=200))
    description = fields.String(validate=validate.Length(min=20, max=5000))
    priority = fields.String(validate=validate.OneOf([
        Ticket.PRIORITY_LOW,
        Ticket.PRIORITY_MEDIUM,
        Ticket.PRIORITY_HIGH,
        Ticket.PRIORITY_URGENT
    ]))
    category = fields.String(validate=validate.OneOf([
        Ticket.CATEGORY_TECHNICAL,
        Ticket.CATEGORY_BILLING,
        Ticket.CATEGORY_GENERAL,
        Ticket.CATEGORY_FEATURE_REQUEST
    ]))
    
    class Meta:
        ordered = True

class TicketStatusUpdateSchema(Schema):
    """Ticket status update schema"""
    status = fields.String(required=True, validate=validate.OneOf([
        Ticket.STATUS_OPEN,
        Ticket.STATUS_ASSIGNED,
        Ticket.STATUS_IN_PROGRESS,
        Ticket.STATUS_WAITING,
        Ticket.STATUS_RESOLVED,
        Ticket.STATUS_CLOSED,
        Ticket.STATUS_REOPENED
    ]))
    notes = fields.String(validate=validate.Length(max=1000))
    
    class Meta:
        ordered = True

class TicketPriorityUpdateSchema(Schema):
    """Ticket priority update schema"""
    priority = fields.String(required=True, validate=validate.OneOf([
        Ticket.PRIORITY_LOW,
        Ticket.PRIORITY_MEDIUM,
        Ticket.PRIORITY_HIGH,
        Ticket.PRIORITY_URGENT
    ]))
    reason = fields.String(required=True, validate=validate.Length(min=10, max=500))
    
    class Meta:
        ordered = True

class TicketAssignSchema(Schema):
    """Ticket assignment schema"""
    assigned_to_id = fields.Integer(required=True)
    notes = fields.String(validate=validate.Length(max=500))
    
    class Meta:
        ordered = True
