from marshmallow import Schema, fields
from flask import url_for
from utils import hash_password


class UserSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    role_id = fields.Int(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Method(required=True, deserialize="load_hashed")
    first_name = fields.Str()
    last_name = fields.Str()
    tax_id = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    photo_url = fields.Method(serialize="dump_photo_url")

    def dump_photo_url(self, user):
        if user.photo:
            return url_for(
                "static",
                filename=f"photos/{user.photo}",
                _external=True,
                _scheme="https",
            )
        else:
            return url_for(
                "static",
                filename="assets/default-photo.jpg",
                _external=True,
                _scheme="https",
            )

    def load_hashed(self, value):
        return hash_password(value)
