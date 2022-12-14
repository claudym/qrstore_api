from marshmallow import Schema, fields, validate
from flask import url_for


class ProductSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    desc = fields.Str(required=True, validate=[validate.Length(max=100)])
    price = fields.Decimal(required=True, as_string=True)
    size_id = fields.Int(required=True)
    sex_id = fields.Int(required=True)
    kid = fields.Boolean(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
    image = fields.Method(serialize="dump_image_url")

    def dump_image_url(self, product):
        if product.image:
            return url_for(
                "static",
                filename=f"products/{product.image}",
                _external=True,
                _scheme="https",
            )
