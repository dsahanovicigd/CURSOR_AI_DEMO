from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.comments import comments_bp
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.schemas.comment import CommentSchema, CommentCreateSchema, CommentUpdateSchema

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
comment_create_schema = CommentCreateSchema()
comment_update_schema = CommentUpdateSchema()

@comments_bp.route('', methods=['GET'])
def get_comments():
    """
    Get all comments
    ---
    tags:
      - Comments
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
        name: post_id
        type: integer
        description: Filter comments by post ID
      - in: query
        name: user_id
        type: integer
        description: Filter comments by user ID
      - in: query
        name: approved_only
        type: boolean
        default: true
        description: Show only approved comments
    responses:
      200:
        description: List of comments
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        post_id = request.args.get('post_id', type=int)
        user_id = request.args.get('user_id', type=int)
        approved_only = request.args.get('approved_only', 'true').lower() == 'true'
        per_page = min(per_page, 100)
        
        query = Comment.query
        
        if post_id:
            query = query.filter_by(post_id=post_id)
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        if approved_only:
            query = query.filter_by(is_approved=True)
        
        comments = query.order_by(Comment.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'comments': comments_schema.dump(comments.items),
            'total': comments.total,
            'pages': comments.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve comments: {str(e)}'}), 500

@comments_bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    """
    Get comment by ID
    ---
    tags:
      - Comments
    parameters:
      - in: path
        name: comment_id
        type: integer
        required: true
    responses:
      200:
        description: Comment information
      404:
        description: Comment not found
    """
    try:
        comment = Comment.query.get_or_404(comment_id)
        
        # Only show unapproved comments to the author or admins
        if not comment.is_approved:
            current_user_id = get_jwt_identity()
            if not current_user_id or (comment.user_id != current_user_id):
                current_user = User.query.get(current_user_id) if current_user_id else None
                if not current_user or not current_user.is_admin_user():
                    return jsonify({'error': 'Comment not found'}), 404
        
        return jsonify(comment_schema.dump(comment)), 200
    except Exception as e:
        if '404' in str(e):
            return jsonify({'error': 'Comment not found'}), 404
        return jsonify({'error': f'Failed to retrieve comment: {str(e)}'}), 500

@comments_bp.route('/post/<int:post_id>', methods=['GET'])
def get_post_comments(post_id):
    """
    Get all comments for a specific post
    ---
    tags:
      - Comments
    parameters:
      - in: path
        name: post_id
        type: integer
        required: true
      - in: query
        name: include_replies
        type: boolean
        default: true
        description: Include nested replies
    responses:
      200:
        description: List of comments for the post
      404:
        description: Post not found
    """
    try:
        post = Post.query.get_or_404(post_id)
        include_replies = request.args.get('include_replies', 'true').lower() == 'true'
        
        query = Comment.query.filter_by(
            post_id=post_id,
            is_approved=True
        )
        
        if not include_replies:
            query = query.filter_by(parent_id=None)
        
        comments = query.order_by(Comment.created_at.asc()).all()
        
        return jsonify(comments_schema.dump(comments)), 200
    except Exception as e:
        if '404' in str(e):
            return jsonify({'error': 'Post not found'}), 404
        return jsonify({'error': f'Failed to retrieve comments: {str(e)}'}), 500

@comments_bp.route('', methods=['POST'])
@jwt_required()
def create_comment():
    """
    Create a new comment
    ---
    tags:
      - Comments
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - content
            - post_id
          properties:
            content:
              type: string
              example: Great post! Thanks for sharing.
            post_id:
              type: integer
              example: 1
            parent_id:
              type: integer
              description: ID of parent comment for nested replies
    responses:
      201:
        description: Comment created successfully
      400:
        description: Validation error
      401:
        description: Unauthorized
      404:
        description: Post not found
    """
    try:
        current_user_id = get_jwt_identity()
        data = comment_create_schema.load(request.json)
        
        # Verify post exists
        post = Post.query.get(data['post_id'])
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # If parent_id is provided, verify parent comment exists and belongs to same post
        if data.get('parent_id'):
            parent_comment = Comment.query.get(data['parent_id'])
            if not parent_comment:
                return jsonify({'error': 'Parent comment not found'}), 404
            if parent_comment.post_id != data['post_id']:
                return jsonify({'error': 'Parent comment does not belong to this post'}), 400
        
        comment = Comment(
            content=data['content'],
            post_id=data['post_id'],
            user_id=current_user_id,
            parent_id=data.get('parent_id')
        )
        
        db.session.add(comment)
        db.session.commit()
        
        return jsonify(comment_schema.dump(comment)), 201
    except Exception as e:
        db.session.rollback()
        if hasattr(e, 'messages'):
            return jsonify({'error': 'Validation error', 'messages': e.messages}), 400
        return jsonify({'error': f'Failed to create comment: {str(e)}'}), 400

@comments_bp.route('/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    """
    Update comment
    ---
    tags:
      - Comments
    security:
      - Bearer: []
    parameters:
      - in: path
        name: comment_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            content:
              type: string
            is_approved:
              type: boolean
              description: Admin only - approve/reject comment
    responses:
      200:
        description: Comment updated successfully
      400:
        description: Validation error
      403:
        description: Forbidden
      404:
        description: Comment not found
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        comment = Comment.query.get_or_404(comment_id)
        
        # Check permissions: author can update content, admin can update approval status
        data = comment_update_schema.load(request.json, partial=True)
        
        if 'is_approved' in data:
            if not current_user or not current_user.is_admin_user():
                return jsonify({'error': 'Forbidden: Admin access required to modify approval status'}), 403
        
        if comment.user_id != current_user_id:
            if not current_user or not current_user.is_admin_user():
                return jsonify({'error': 'Forbidden: You can only update your own comments'}), 403
        
        # Non-admins can only update content
        if not current_user or not current_user.is_admin_user():
            data = {k: v for k, v in data.items() if k == 'content'}
        
        for key, value in data.items():
            setattr(comment, key, value)
        
        db.session.commit()
        
        return jsonify(comment_schema.dump(comment)), 200
    except Exception as e:
        db.session.rollback()
        if '404' in str(e):
            return jsonify({'error': 'Comment not found'}), 404
        if hasattr(e, 'messages'):
            return jsonify({'error': 'Validation error', 'messages': e.messages}), 400
        return jsonify({'error': f'Failed to update comment: {str(e)}'}), 400

@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """
    Delete comment
    ---
    tags:
      - Comments
    security:
      - Bearer: []
    parameters:
      - in: path
        name: comment_id
        type: integer
        required: true
    responses:
      204:
        description: Comment deleted successfully
      403:
        description: Forbidden
      404:
        description: Comment not found
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        comment = Comment.query.get_or_404(comment_id)
        
        # Check permissions: author or admin can delete
        if comment.user_id != current_user_id:
            if not current_user or not current_user.is_admin_user():
                return jsonify({'error': 'Forbidden: You can only delete your own comments'}), 403
        
        db.session.delete(comment)
        db.session.commit()
        
        return '', 204
    except Exception as e:
        db.session.rollback()
        if '404' in str(e):
            return jsonify({'error': 'Comment not found'}), 404
        return jsonify({'error': f'Failed to delete comment: {str(e)}'}), 500
