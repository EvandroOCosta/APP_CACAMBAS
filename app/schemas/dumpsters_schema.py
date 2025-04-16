#schemas/dumpsters_schema.py

from marshmallow import Schema, fields, validate

class DumpsterSchema(Schema):
    id = fields.Int(dump_only=True)
    location = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="A localização é obrigatória.")
    )
    size = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="O tamanho é obrigatório.")
    )
