from marshmallow import Schema, fields
from utils import hash_password


class UserSchema(Schema):
    class Meta:
        ordered = True
    
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    hashed = fields.Method(required=True, deserialize='load_hashed')
    first_name = fields.Str()
    last_name = fields.Str()
    tax_id = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    def load_hashed(self, value):
        return hash_password(value)
