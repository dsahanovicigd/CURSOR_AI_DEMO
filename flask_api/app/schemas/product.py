"""Product schemas"""
from marshmallow import Schema, fields, validate, validates, ValidationError


class ProductSchema(Schema):
    """Product schema"""
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(allow_none=True)
    price = fields.Decimal(required=True, places=2, validate=validate.Range(min=0))
    original_price = fields.Decimal(allow_none=True, places=2, validate=validate.Range(min=0))
    currency = fields.String(missing='USD', validate=validate.Length(max=10))
    image = fields.String(allow_none=True, validate=validate.Length(max=500))
    stock = fields.Integer(missing=0, validate=validate.Range(min=0))
    in_stock = fields.Boolean(missing=True)
    category = fields.String(allow_none=True, validate=validate.Length(max=100))
    sku = fields.String(allow_none=True, validate=validate.Length(max=100))
    colors = fields.List(fields.String(), allow_none=True)
    sizes = fields.List(fields.String(), allow_none=True)
    rating_average = fields.Decimal(places=2, missing=0.0, validate=validate.Range(min=0, max=5))
    rating_count = fields.Integer(missing=0, validate=validate.Range(min=0))
    badge_type = fields.String(allow_none=True, validate=validate.OneOf(['sale', 'new', 'trending', 'limited', 'bestseller']))
    badge_text = fields.String(allow_none=True, validate=validate.Length(max=100))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ProductCreateSchema(Schema):
    """Product creation schema"""
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(allow_none=True)
    price = fields.Decimal(required=True, places=2, validate=validate.Range(min=0))
    original_price = fields.Decimal(allow_none=True, places=2, validate=validate.Range(min=0))
    currency = fields.String(missing='USD')
    image = fields.String(allow_none=True)
    stock = fields.Integer(missing=0, validate=validate.Range(min=0))
    category = fields.String(allow_none=True)
    sku = fields.String(allow_none=True)
    colors = fields.List(fields.String(), allow_none=True)
    sizes = fields.List(fields.String(), allow_none=True)
    badge_type = fields.String(allow_none=True, validate=validate.OneOf(['sale', 'new', 'trending', 'limited', 'bestseller']))
    badge_text = fields.String(allow_none=True)
