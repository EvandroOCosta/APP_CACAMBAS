# schemas/review_schema.py
from marshmallow import Schema, fields, validate

class ReviewSchema(Schema):
    user_id = fields.Int(required=True, error_messages={"required": "O campo user_id é obrigatório."})
    dumpster_id = fields.Int(required=True, error_messages={"required": "O campo dumpster_id é obrigatório."})
    rating = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=5, error="A avaliação deve ser entre 1 e 5."),
        error_messages={"required": "O campo rating é obrigatório."}
    )
    comment = fields.Str(
        required=True,
        validate=validate.Length(max=500, error="O comentário pode ter no máximo 500 caracteres."),
        error_messages={"required": "O campo comment é obrigatório."}
    )
