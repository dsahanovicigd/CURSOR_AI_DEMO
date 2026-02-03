"""HTML sanitization utilities for XSS protection"""
import bleach
from markupsafe import Markup

# Allowed HTML tags for user-generated content
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'b', 'i',
    'ul', 'ol', 'li', 'blockquote', 'code', 'pre'
]

# Allowed HTML attributes
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'code': ['class'],
    'pre': ['class']
}

# Allowed URL schemes
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


def sanitize_html(content):
    """
    Sanitize HTML content to prevent XSS attacks
    
    Args:
        content: HTML string to sanitize
        
    Returns:
        Sanitized HTML string
    """
    if not content:
        return ''
    
    # Clean HTML content
    cleaned = bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True
    )
    
    return cleaned


def sanitize_text(content):
    """
    Strip all HTML tags from content (for plain text fields)
    
    Args:
        content: Text content that may contain HTML
        
    Returns:
        Plain text without HTML tags
    """
    if not content:
        return ''
    
    return bleach.clean(content, tags=[], strip=True)


def sanitize_user_input(data, fields_to_sanitize=None):
    """
    Sanitize user input data dictionary
    
    Args:
        data: Dictionary of user input
        fields_to_sanitize: List of field names to sanitize (None = all text fields)
        
    Returns:
        Dictionary with sanitized values
    """
    if not isinstance(data, dict):
        return data
    
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            if fields_to_sanitize is None or key in fields_to_sanitize:
                # Sanitize HTML for content fields, strip HTML for others
                if key in ['content', 'description', 'notes']:
                    sanitized[key] = sanitize_html(value)
                else:
                    sanitized[key] = sanitize_text(value)
            else:
                sanitized[key] = value
        else:
            sanitized[key] = value
    
    return sanitized
