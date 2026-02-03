from marshmallow import Schema, fields, validate
from app.models.notification import Notification

class NotificationSchema(Schema):
    """Notification serialization schema"""
    id = fields.Integer(dump_only=True)
    type = fields.String(validate=validate.OneOf([
        Notification.TYPE_TASK_ASSIGNED,
        Notification.TYPE_TASK_COMPLETED,
        Notification.TYPE_TASK_COMMENT,
        Notification.TYPE_PROJECT_INVITE,
        Notification.TYPE_TEAM_INVITE,
        Notification.TYPE_MENTION,
        Notification.TYPE_DUE_DATE_REMINDER
    ]))
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    message = fields.String(required=True, validate=validate.Length(min=1))
    is_read = fields.Boolean(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    related_task_id = fields.Integer(allow_none=True)
    related_project_id = fields.Integer(allow_none=True)
    related_team_id = fields.Integer(allow_none=True)
    metadata = fields.Dict(allow_none=True, attribute='meta_data', data_key='metadata')
    created_at = fields.DateTime(dump_only=True)
    read_at = fields.DateTime(dump_only=True)
    
    class Meta:
        ordered = True

class NotificationCreateSchema(Schema):
    """Notification creation schema"""
    type = fields.String(required=True, validate=validate.OneOf([
        Notification.TYPE_TASK_ASSIGNED,
        Notification.TYPE_TASK_COMPLETED,
        Notification.TYPE_TASK_COMMENT,
        Notification.TYPE_PROJECT_INVITE,
        Notification.TYPE_TEAM_INVITE,
        Notification.TYPE_MENTION,
        Notification.TYPE_DUE_DATE_REMINDER
    ]))
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    message = fields.String(required=True, validate=validate.Length(min=1))
    user_id = fields.Integer(required=True)
    related_task_id = fields.Integer(allow_none=True)
    related_project_id = fields.Integer(allow_none=True)
    related_team_id = fields.Integer(allow_none=True)
    metadata = fields.Dict(allow_none=True, attribute='meta_data', data_key='metadata')
    
    class Meta:
        ordered = True
