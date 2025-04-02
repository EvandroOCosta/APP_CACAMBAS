from marshmallow import Schema, fields, validate

class ReviewSchema(Schema):
    user_id = fields.Int(required=True)
    dumpster_id = fields.Int(required=True)
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.Str(required=True, validate=validate.Length(max=500))
    # review_text = fields.Str(required=True)
    # comment = fields.Str(required=True)


