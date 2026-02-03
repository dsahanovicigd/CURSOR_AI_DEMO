from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime
from app.models.task import Task

class TaskSchema(Schema):
    """Task serialization schema"""
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(validate=validate.Length(max=5000))
    status = fields.String(validate=validate.OneOf([
        Task.STATUS_PENDING,
        Task.STATUS_IN_PROGRESS,
        Task.STATUS_COMPLETED,
        Task.STATUS_CANCELLED
    ]))
    priority = fields.String(validate=validate.OneOf([
        Task.PRIORITY_LOW,
        Task.PRIORITY_MEDIUM,
        Task.PRIORITY_HIGH,
        Task.PRIORITY_URGENT
    ]))
    project_id = fields.Integer(allow_none=True)
    project_name = fields.String(dump_only=True)
    assigned_to_id = fields.Integer(allow_none=True)
    assigned_to_name = fields.String(dump_only=True)
    created_by_id = fields.Integer(dump_only=True)
    created_by_name = fields.String(dump_only=True)
    due_date = fields.DateTime(allow_none=True)
    completed_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    comment_count = fields.Integer(dump_only=True)
    attachment_count = fields.Integer(dump_only=True)
    
    class Meta:
        ordered = True

class TaskCreateSchema(Schema):
    """Task creation schema"""
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(validate=validate.Length(max=5000))
    status = fields.String(load_default=Task.STATUS_PENDING, validate=validate.OneOf([
        Task.STATUS_PENDING,
        Task.STATUS_IN_PROGRESS,
        Task.STATUS_COMPLETED,
        Task.STATUS_CANCELLED
    ]))
    priority = fields.String(load_default=Task.PRIORITY_MEDIUM, validate=validate.OneOf([
        Task.PRIORITY_LOW,
        Task.PRIORITY_MEDIUM,
        Task.PRIORITY_HIGH,
        Task.PRIORITY_URGENT
    ]))
    project_id = fields.Integer(allow_none=True)
    assigned_to_id = fields.Integer(allow_none=True)
    due_date = fields.DateTime(allow_none=True)
    
    class Meta:
        ordered = True

class TaskUpdateSchema(Schema):
    """Task update schema"""
    title = fields.String(validate=validate.Length(min=1, max=200))
    description = fields.String(validate=validate.Length(max=5000))
    status = fields.String(validate=validate.OneOf([
        Task.STATUS_PENDING,
        Task.STATUS_IN_PROGRESS,
        Task.STATUS_COMPLETED,
        Task.STATUS_CANCELLED
    ]))
    priority = fields.String(validate=validate.OneOf([
        Task.PRIORITY_LOW,
        Task.PRIORITY_MEDIUM,
        Task.PRIORITY_HIGH,
        Task.PRIORITY_URGENT
    ]))
    project_id = fields.Integer(allow_none=True)
    assigned_to_id = fields.Integer(allow_none=True)
    due_date = fields.DateTime(allow_none=True)
    
    class Meta:
        ordered = True
