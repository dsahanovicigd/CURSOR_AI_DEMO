"""Cart schemas"""
from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    """Product schema for cart items"""
    id = fields.Integer(dump_only=True)
    title = fields.String(dump_only=True)
    price = fields.Decimal(dump_only=True, places=2)
    image = fields.String(dump_only=True)
    in_stock = fields.Boolean(dump_only=True)


class CartItemSchema(Schema):
    """Cart item schema"""
    id = fields.Integer(dump_only=True)
    cart_id = fields.Integer(dump_only=True)
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))
    subtotal = fields.Decimal(dump_only=True, places=2)
    product = fields.Nested(ProductSchema, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CartSchema(Schema):
    """Cart schema"""
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    items = fields.Nested(CartItemSchema, many=True, dump_only=True)
    subtotal = fields.Decimal(dump_only=True, places=2)
    discount_code = fields.String(allow_none=True, dump_only=True)
    discount_amount = fields.Decimal(dump_only=True, places=2)
    total = fields.Decimal(dump_only=True, places=2)
    item_count = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class AddToCartSchema(Schema):
    """Add to cart schema"""
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))


class UpdateCartItemSchema(Schema):
    """Update cart item schema"""
    quantity = fields.Integer(required=True, validate=validate.Range(min=0))


class ApplyDiscountSchema(Schema):
    """Apply discount code schema"""
    discount_code = fields.String(required=True, validate=validate.Length(min=1, max=50))
