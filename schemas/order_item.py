from marshmallow import Schema, fields, validates, ValidationError


class OrderItemSchema(Schema):
    class Meta:
        ordered = True

    order_id = fields.Int(load_only=True)
    product_id = fields.Int(required=True, load_only=True)
    product_snapshot_id = fields.Int(dump_only=True)
    count = fields.Int(required=True)

    @validates("count")
    def validate_count(self, value):
        if value < 0:
            raise ValidationError("Count cannot be negative")
