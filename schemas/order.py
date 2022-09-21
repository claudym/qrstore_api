from marshmallow import Schema, fields, validate
from schemas.order_item import OrderItemSchema


class OrderSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    total = fields.Decimal(dump_only=True, as_string=True)
    order_status_id = fields.Int(dump_only=True)
    payment_method_id = fields.Int(required=True)
    payment = fields.Decimal(required=True, as_string=True)
    customer_name = fields.Str(validate=[validate.Length(max=100)])
    customer_phone = fields.Str(validate=[validate.Length(max=20)])
    customer_email = fields.Email(validate=[validate.Length(max=100)])
    tax_id = fields.Str(validate=[validate.Length(max=50)])
    order_items = fields.List(fields.Nested(OrderItemSchema))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
