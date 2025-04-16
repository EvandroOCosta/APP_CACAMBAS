# schemas/user_schema.py
from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="O nome é obrigatório.")
    )
    email = fields.Email(
        required=True,
        error_messages={"required": "O e-mail é obrigatório."}
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=6, error="A senha deve ter no mínimo 6 caracteres.")
    )
