from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.notifications import notifications_bp
from app.models.notification import Notification
from app.schemas.notification import NotificationSchema

notification_schema = NotificationSchema()
notifications_schema = NotificationSchema(many=True)

@notifications_bp.route('', methods=['GET'])
@jwt_required()
def get_notifications():
    """
    Get all notifications for current user
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: per_page
        type: integer
        default: 20
      - in: query
        name: is_read
        type: boolean
      - in: query
        name: type
        type: string
    responses:
      200:
        description: List of notifications
    """
    current_user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    is_read = request.args.get('is_read', type=lambda x: x.lower() == 'true' if x else None)
    notification_type = request.args.get('type')
    per_page = min(per_page, 100)
    
    query = Notification.query.filter_by(user_id=current_user_id)
    
    if is_read is not None:
        query = query.filter_by(is_read=is_read)
    
    if notification_type:
        query = query.filter_by(type=notification_type)
    
    notifications = query.order_by(Notification.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'notifications': notifications_schema.dump(notifications.items),
        'pagination': {
            'page': notifications.page,
            'pages': notifications.pages,
            'per_page': notifications.per_page,
            'total': notifications.total
        },
        'unread_count': Notification.query.filter_by(user_id=current_user_id, is_read=False).count()
    }), 200

@notifications_bp.route('/<int:notification_id>', methods=['GET'])
@jwt_required()
def get_notification(notification_id):
    """
    Get a specific notification
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    parameters:
      - in: path
        name: notification_id
        type: integer
        required: true
    responses:
      200:
        description: Notification details
      403:
        description: Access denied
      404:
        description: Notification not found
    """
    current_user_id = get_jwt_identity()
    notification = Notification.query.get_or_404(notification_id)
    
    # Check ownership
    if notification.user_id != current_user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify(notification_schema.dump(notification)), 200

@notifications_bp.route('/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_notification_read(notification_id):
    """
    Mark a notification as read
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    parameters:
      - in: path
        name: notification_id
        type: integer
        required: true
    responses:
      200:
        description: Notification marked as read
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    notification = Notification.query.get_or_404(notification_id)
    
    # Check ownership
    if notification.user_id != current_user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    notification.mark_as_read()
    db.session.commit()
    
    return jsonify(notification_schema.dump(notification)), 200

@notifications_bp.route('/read-all', methods=['POST'])
@jwt_required()
def mark_all_notifications_read():
    """
    Mark all notifications as read
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    responses:
      200:
        description: All notifications marked as read
    """
    current_user_id = get_jwt_identity()
    
    notifications = Notification.query.filter_by(user_id=current_user_id, is_read=False).all()
    for notification in notifications:
        notification.mark_as_read()
    
    db.session.commit()
    
    return jsonify({'message': f'{len(notifications)} notifications marked as read'}), 200

@notifications_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """
    Get unread notification count
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    responses:
      200:
        description: Unread notification count
    """
    current_user_id = get_jwt_identity()
    
    count = Notification.query.filter_by(user_id=current_user_id, is_read=False).count()
    
    return jsonify({'unread_count': count}), 200
