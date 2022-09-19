from marshmallow import Schema, fields


class OrderStatusSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    desc = fields.Str(required=True)
