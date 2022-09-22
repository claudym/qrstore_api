from marshmallow import Schema, fields


class ProductSnapshotSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    product_id = fields.Int(dump_only=True)
    desc = fields.Str(dump_only=True)
    price = fields.Decimal(dump_only=True, as_string=True)
    size_id = fields.Int(dump_only=True)
    sex_id = fields.Int(dump_only=True)
    kid = fields.Boolean(dump_only=True)
    user_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
