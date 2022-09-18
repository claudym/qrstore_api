from marshmallow import Schema, fields


class SexSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    desc = fields.Str(required=True)
