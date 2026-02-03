from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_, and_
from app import db
from app.posts import posts_bp
from app.models.post import Post
from app.models.category import Category
from app.models.comment import Comment
from app.models.user import User
from app.schemas.post import PostSchema, PostCreateSchema, PostUpdateSchema
from app.schemas.comment import CommentSchema, CommentCreateSchema
from app.cache_utils import cached_post_list, cached_post_detail, cached_search, invalidate_post_cache, invalidate_comment_cache
# Import optimized functions if available
try:
    from app.cache_utils_optimized import (
        invalidate_post_cache as invalidate_post_cache_optimized,
        invalidate_comment_cache as invalidate_comment_cache_optimized,
        warm_cache_for_popular_posts,
        get_cache_stats
    )
    USE_OPTIMIZED_CACHE = True
except ImportError:
    USE_OPTIMIZED_CACHE = False

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
post_create_schema = PostCreateSchema()
post_update_schema = PostUpdateSchema()

@posts_bp.route('', methods=['GET'])
@cached_post_list(timeout=300)  # 5 minutes - optimized for list queries
def get_posts():
    """
    Get all posts with search and filtering
    ---
    tags:
      - Posts
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
        name: user_id
        type: integer
        description: Filter by author user ID
      - in: query
        name: category_id
        type: integer
        description: Filter by category ID
      - in: query
        name: search
        type: string
        description: Search in title and content
      - in: query
        name: tag
        type: string
        description: Filter by tag
      - in: query
        name: published_only
        type: boolean
        default: true
        description: Show only published posts
    responses:
      200:
        description: List of posts
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        user_id = request.args.get('user_id', type=int)
        category_id = request.args.get('category_id', type=int)
        search = request.args.get('search', '', type=str).strip()
        tag = request.args.get('tag', '', type=str).strip()
        published_only = request.args.get('published_only', 'true').lower() == 'true'
        per_page = min(per_page, 100)
        
        query = Post.query
        
        # Filter by published status
        if published_only:
            query = query.filter_by(is_published=True)
        
        # Filter by user
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        # Filter by category
        if category_id:
            category = Category.query.get(category_id)
            if category:
                query = query.filter(Post.categories.contains(category))
        
        # Search functionality
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                or_(
                    Post.title.ilike(search_pattern),
                    Post.content.ilike(search_pattern),
                    Post.excerpt.ilike(search_pattern)
                )
            )
        
        # Filter by tag
        if tag:
            query = query.filter(Post.tags.ilike(f'%{tag}%'))
        
        posts = query.order_by(Post.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'posts': [post.to_dict() for post in posts.items],
            'total': posts.total,
            'pages': posts.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve posts: {str(e)}'}), 500

@posts_bp.route('/search', methods=['GET'])
@cached_search(timeout=300)
def search_posts():
    """
    Advanced search for posts
    ---
    tags:
      - Posts
    parameters:
      - in: query
        name: q
        type: string
        required: true
        description: Search query
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: per_page
        type: integer
        default: 20
      - in: query
        name: category_id
        type: integer
        description: Filter by category
      - in: query
        name: tag
        type: string
        description: Filter by tag
    responses:
      200:
        description: Search results
      400:
        description: Invalid search query
    """
    try:
        search_query = request.args.get('q', '', type=str).strip()
        if not search_query:
            return jsonify({'error': 'Search query is required'}), 400
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category_id = request.args.get('category_id', type=int)
        tag = request.args.get('tag', '', type=str).strip()
        per_page = min(per_page, 100)
        
        query = Post.query.filter_by(is_published=True)
        
        # Search in title, content, and excerpt
        search_pattern = f'%{search_query}%'
        query = query.filter(
            or_(
                Post.title.ilike(search_pattern),
                Post.content.ilike(search_pattern),
                Post.excerpt.ilike(search_pattern)
            )
        )
        
        # Filter by category
        if category_id:
            category = Category.query.get(category_id)
            if category:
                query = query.filter(Post.categories.contains(category))
        
        # Filter by tag
        if tag:
            query = query.filter(Post.tags.ilike(f'%{tag}%'))
        
        posts = query.order_by(Post.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'query': search_query,
            'posts': [post.to_dict() for post in posts.items],
            'total': posts.total,
            'pages': posts.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@posts_bp.route('/<int:post_id>', methods=['GET'])
@cached_post_detail(timeout=600)
def get_post(post_id):
    """
    Get post by ID
    ---
    tags:
      - Posts
    parameters:
      - in: path
        name: post_id
        type: integer
        required: true
      - in: query
        name: include_comments
        type: boolean
        default: false
        description: Include comments in response
    responses:
      200:
        description: Post information
      404:
        description: Post not found
    """
    try:
        include_comments = request.args.get('include_comments', 'false').lower() == 'true'
        post = Post.query.get_or_404(post_id)
        
        # Check if user can view unpublished post
        if not post.is_published:
            try:
                current_user_id = get_jwt_identity()
            except Exception:
                current_user_id = None
            
            if not current_user_id or post.user_id != current_user_id:
                current_user = User.query.get(current_user_id) if current_user_id else None
                if not current_user or not current_user.is_admin_user():
                    return jsonify({'error': 'Post not found'}), 404
        
        # Increment view count
        post.view_count += 1
        db.session.commit()
        
        post_dict = post.to_dict(include_comments=include_comments)
        return jsonify(post_dict), 200
    except Exception as e:
        db.session.rollback()
        if '404' in str(e):
            return jsonify({'error': 'Post not found'}), 404
        return jsonify({'error': f'Failed to retrieve post: {str(e)}'}), 500

@posts_bp.route('/slug/<slug>', methods=['GET'])
@cached_post_detail(timeout=600)
def get_post_by_slug(slug):
    """
    Get post by slug
    ---
    tags:
      - Posts
    parameters:
      - in: path
        name: slug
        type: string
        required: true
      - in: query
        name: include_comments
        type: boolean
        default: false
        description: Include comments in response
    responses:
      200:
        description: Post information
      404:
        description: Post not found
    """
    try:
        include_comments = request.args.get('include_comments', 'false').lower() == 'true'
        post = Post.query.filter_by(slug=slug).first_or_404()
        
        # Check if user can view unpublished post
        if not post.is_published:
            try:
                current_user_id = get_jwt_identity()
            except Exception:
                current_user_id = None
            
            if not current_user_id or post.user_id != current_user_id:
                current_user = User.query.get(current_user_id) if current_user_id else None
                if not current_user or not current_user.is_admin_user():
                    return jsonify({'error': 'Post not found'}), 404
        
        # Increment view count
        post.view_count += 1
        db.session.commit()
        
        post_dict = post.to_dict(include_comments=include_comments)
        return jsonify(post_dict), 200
    except Exception as e:
        db.session.rollback()
        if '404' in str(e):
            return jsonify({'error': 'Post not found'}), 404
        return jsonify({'error': f'Failed to retrieve post: {str(e)}'}), 500

@posts_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    """
    Create a new post
    ---
    tags:
      - Posts
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - title
            - content
          properties:
            title:
              type: string
              example: My First Post
            content:
              type: string
              example: This is the content of my post
            excerpt:
              type: string
              example: A brief summary of the post
            is_published:
              type: boolean
              default: true
            tags:
              type: array
              items:
                type: string
              example: ["python", "flask", "api"]
            category_ids:
              type: array
              items:
                type: integer
              example: [1, 2]
    responses:
      201:
        description: Post created successfully
      400:
        description: Validation error
      401:
        description: Unauthorized
    """
    try:
        current_user_id = get_jwt_identity()
        data = post_create_schema.load(request.json)
        
        # Generate slug from title
        slug = Post.generate_slug(data['title'])
        
        # Ensure slug is unique
        counter = 1
        base_slug = slug
        while Post.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Process tags
        tags_str = None
        if data.get('tags'):
            tags_str = ','.join([tag.strip() for tag in data['tags'] if tag.strip()])
        
        post = Post(
            title=data['title'],
            slug=slug,
            content=data['content'],
            excerpt=data.get('excerpt'),
            user_id=current_user_id,
            is_published=data.get('is_published', True),
            tags=tags_str
        )
        
        # Add categories
        if data.get('category_ids'):
            categories = Category.query.filter(Category.id.in_(data['category_ids'])).all()
            # Validate that all provided category IDs exist
            found_category_ids = {cat.id for cat in categories}
            requested_category_ids = set(data['category_ids'])
            missing_category_ids = requested_category_ids - found_category_ids
            if missing_category_ids:
                return jsonify({
                    'error': 'Validation error',
                    'messages': {'category_ids': [f'Category IDs {sorted(missing_category_ids)} do not exist']}
                }), 400
            post.categories = categories
        
        db.session.add(post)
        db.session.commit()
        
        # Invalidate cache (use optimized version if available)
        if USE_OPTIMIZED_CACHE:
            invalidate_post_cache_optimized(user_id=current_user_id, selective=True)
        else:
            invalidate_post_cache(user_id=current_user_id)
        
        return jsonify(post.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        if hasattr(e, 'messages'):
            return jsonify({'error': 'Validation error', 'messages': e.messages}), 400
        return jsonify({'error': f'Failed to create post: {str(e)}'}), 400

@posts_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    """
    Update post
    ---
    tags:
      - Posts
    security:
      - Bearer: []
    parameters:
      - in: path
        name: post_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            title:
              type: string
            content:
              type: string
            excerpt:
              type: string
            is_published:
              type: boolean
            tags:
              type: array
              items:
                type: string
            category_ids:
              type: array
              items:
                type: integer
    responses:
      200:
        description: Post updated successfully
      400:
        description: Validation error
      403:
        description: Forbidden
      404:
        description: Post not found
    """
    try:
        post = Post.query.get_or_404(post_id)
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if post.user_id != current_user_id and (not current_user or not current_user.is_admin_user()):
            return jsonify({'error': 'Forbidden: You can only update your own posts'}), 403
        
        data = post_update_schema.load(request.json, partial=True)
        
        # If title is updated, regenerate slug
        if 'title' in data:
            slug = Post.generate_slug(data['title'])
            # Ensure slug is unique
            counter = 1
            base_slug = slug
            while Post.query.filter(Post.slug == slug, Post.id != post_id).first():
                slug = f"{base_slug}-{counter}"
                counter += 1
            data['slug'] = slug
        
        # Process tags
        if 'tags' in data:
            if data['tags']:
                data['tags'] = ','.join([tag.strip() for tag in data['tags'] if tag.strip()])
            else:
                data['tags'] = None
        
        # Update categories
        if 'category_ids' in data:
            if data['category_ids']:
                categories = Category.query.filter(Category.id.in_(data['category_ids'])).all()
                # Validate that all provided category IDs exist
                found_category_ids = {cat.id for cat in categories}
                requested_category_ids = set(data['category_ids'])
                missing_category_ids = requested_category_ids - found_category_ids
                if missing_category_ids:
                    return jsonify({
                        'error': 'Validation error',
                        'messages': {'category_ids': [f'Category IDs {sorted(missing_category_ids)} do not exist']}
                    }), 400
                post.categories = categories
            else:
                post.categories = []
            # Remove category_ids from data dict since it's not a column
            del data['category_ids']
        
        # Remove tags from data dict and handle separately
        tags_value = data.pop('tags', None)
        if tags_value is not None:
            post.tags = tags_value
        
        for key, value in data.items():
            setattr(post, key, value)
        
        db.session.commit()
        
        # Invalidate cache for this post and lists (use optimized version if available)
        if USE_OPTIMIZED_CACHE:
            invalidate_post_cache_optimized(post_id=post_id, slug=post.slug, user_id=post.user_id, selective=True)
        else:
            invalidate_post_cache(post_id=post_id, slug=post.slug, user_id=post.user_id)
        
        return jsonify(post.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        if '404' in str(e):
            return jsonify({'error': 'Post not found'}), 404
        if hasattr(e, 'messages'):
            return jsonify({'error': 'Validation error', 'messages': e.messages}), 400
        return jsonify({'error': f'Failed to update post: {str(e)}'}), 400

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """
    Delete post
    ---
    tags:
      - Posts
    security:
      - Bearer: []
    parameters:
      - in: path
        name: post_id
        type: integer
        required: true
    responses:
      204:
        description: Post deleted successfully
      403:
        description: Forbidden
      404:
        description: Post not found
    """
    try:
        post = Post.query.get_or_404(post_id)
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if post.user_id != current_user_id and (not current_user or not current_user.is_admin_user()):
            return jsonify({'error': 'Forbidden: You can only delete your own posts'}), 403
        
        post_id_to_delete = post.id
        post_slug = post.slug
        post_user_id = post.user_id
        
        db.session.delete(post)
        db.session.commit()
        
        # Invalidate cache (use optimized version if available)
        if USE_OPTIMIZED_CACHE:
            invalidate_post_cache_optimized(post_id=post_id_to_delete, slug=post_slug, user_id=post_user_id, selective=True)
            invalidate_comment_cache_optimized(post_id=post_id_to_delete)
        else:
            invalidate_post_cache(post_id=post_id_to_delete, slug=post_slug, user_id=post_user_id)
            invalidate_comment_cache(post_id=post_id_to_delete)
        
        return '', 204
    except Exception as e:
        db.session.rollback()
        if '404' in str(e):
            return jsonify({'error': 'Post not found'}), 404
        return jsonify({'error': f'Failed to delete post: {str(e)}'}), 500

@posts_bp.route('/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    """
    Get all comments for a specific post
    ---
    tags:
      - Posts
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
        comment_schema = CommentSchema(many=True)
        
        return jsonify(comment_schema.dump(comments)), 200
    except Exception as e:
        if '404' in str(e):
            return jsonify({'error': 'Post not found'}), 404
        return jsonify({'error': f'Failed to retrieve comments: {str(e)}'}), 500

@posts_bp.route('/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_post_comment(post_id):
    """
    Create a new comment on a post
    ---
    tags:
      - Posts
    security:
      - Bearer: []
    parameters:
      - in: path
        name: post_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - content
          properties:
            content:
              type: string
              example: Great post! Thanks for sharing.
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
        
        # Verify post exists
        post = Post.query.get_or_404(post_id)
        
        comment_create_schema = CommentCreateSchema()
        data = comment_create_schema.load(request.json)
        
        # If parent_id is provided, verify parent comment exists and belongs to same post
        if data.get('parent_id'):
            parent_comment = Comment.query.get(data['parent_id'])
            if not parent_comment:
                return jsonify({'error': 'Parent comment not found'}), 404
            if parent_comment.post_id != post_id:
                return jsonify({'error': 'Parent comment does not belong to this post'}), 400
        
        comment = Comment(
            content=data['content'],
            post_id=post_id,
            user_id=current_user_id,
            parent_id=data.get('parent_id')
        )
        
        db.session.add(comment)
        db.session.commit()
        
        # Invalidate comment cache for this post (use optimized version if available)
        if USE_OPTIMIZED_CACHE:
            invalidate_comment_cache_optimized(post_id=post_id)
            invalidate_post_cache_optimized(post_id=post_id, selective=True)
        else:
            invalidate_comment_cache(post_id=post_id)
            invalidate_post_cache(post_id=post_id)
        
        comment_schema = CommentSchema()
        return jsonify(comment_schema.dump(comment)), 201
    except Exception as e:
        db.session.rollback()
        if '404' in str(e):
            return jsonify({'error': 'Post not found'}), 404
        if hasattr(e, 'messages'):
            return jsonify({'error': 'Validation error', 'messages': e.messages}), 400
        return jsonify({'error': f'Failed to create comment: {str(e)}'}), 400
