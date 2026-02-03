"""Order schemas"""
from marshmallow import Schema, fields, validate, validates, ValidationError


class ShippingAddressSchema(Schema):
    """Shipping address schema"""
    full_name = fields.String(required=True, validate=validate.Length(min=1, max=200))
    street = fields.String(required=True, validate=validate.Length(min=1, max=200))
    city = fields.String(required=True, validate=validate.Length(min=1, max=100))
    state = fields.String(required=True, validate=validate.Length(min=1, max=100))
    zip = fields.String(required=True, validate=validate.Length(min=1, max=20))
    country = fields.String(required=True, validate=validate.Length(min=1, max=100))
    phone = fields.String(allow_none=True, validate=validate.Length(max=20))


class PaymentDataSchema(Schema):
    """Payment data schema"""
    card_number = fields.String(required=True, validate=validate.Length(min=13, max=19))
    cardholder_name = fields.String(required=True, validate=validate.Length(min=1, max=200))
    expiry_month = fields.Integer(required=True, validate=validate.Range(min=1, max=12))
    expiry_year = fields.Integer(required=True, validate=validate.Range(min=2020, max=2100))
    cvv = fields.String(required=True, validate=validate.Length(min=3, max=4))
    billing_address = fields.Nested(ShippingAddressSchema, allow_none=True)


class OrderItemSchema(Schema):
    """Order item schema"""
    id = fields.Integer(dump_only=True)
    order_id = fields.Integer(dump_only=True)
    product_id = fields.Integer(dump_only=True)
    product_title = fields.String(dump_only=True)
    product_price = fields.Decimal(dump_only=True, places=2)
    product_sku = fields.String(allow_none=True, dump_only=True)
    quantity = fields.Integer(dump_only=True)
    subtotal = fields.Decimal(dump_only=True, places=2)


class OrderSchema(Schema):
    """Order schema"""
    id = fields.Integer(dump_only=True)
    order_number = fields.String(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    items = fields.Nested(OrderItemSchema, many=True, dump_only=True)
    subtotal = fields.Decimal(dump_only=True, places=2)
    tax = fields.Decimal(dump_only=True, places=2)
    shipping = fields.Decimal(dump_only=True, places=2)
    discount_amount = fields.Decimal(dump_only=True, places=2)
    discount_code = fields.String(allow_none=True, dump_only=True)
    total = fields.Decimal(dump_only=True, places=2)
    status = fields.String(dump_only=True)
    payment_status = fields.String(dump_only=True)
    transaction_id = fields.String(allow_none=True, dump_only=True)
    payment_method = fields.String(dump_only=True)
    shipping_address = fields.Dict(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    confirmed_at = fields.DateTime(allow_none=True, dump_only=True)
    shipped_at = fields.DateTime(allow_none=True, dump_only=True)
    delivered_at = fields.DateTime(allow_none=True, dump_only=True)


class CheckoutSchema(Schema):
    """Checkout schema"""
    payment = fields.Nested(PaymentDataSchema, required=True)
    shipping_address = fields.Nested(ShippingAddressSchema, required=True)
