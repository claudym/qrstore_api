from marshmallow import Schema, fields, validates, ValidationError


class InventorySchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    user_id = fields.Int(dump_only=True)
    count = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates("count")
    def validate_count(self, value):
        if value < 0:
            raise ValidationError("Count should cannot be negative")
