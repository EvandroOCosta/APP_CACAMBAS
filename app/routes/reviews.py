#routes/reviews.py
from flask import Blueprint, request, jsonify
from config.database import db
from app.models.review import Review
from app.schemas.review_schema import ReviewSchema

bp = Blueprint('reviews', __name__)
schema = ReviewSchema()

# GET - Listar todas as avaliações
@bp.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([{
        "id": r.id,
        "comment": r.comment,
        "rating": r.rating,
        "user_id": r.user_id
    } for r in reviews])

# GET - Obter uma avaliação por ID
@bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Avaliação não encontrada"}), 404
    return jsonify({
        "id": review.id,
        "comment": review.comment,
        "rating": review.rating,
        "user_id": review.user_id
    })

# POST - Criar uma nova avaliação
@bp.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    errors = schema.validate(data)

    if errors:
        return jsonify({"errors": errors}), 400

    new_review = Review(
        comment=data["comment"],
        rating=data["rating"],
        user_id=data["user_id"]
    )

    try:
        db.session.add(new_review)
        db.session.commit()
        return jsonify({
            "id": new_review.id,
            "comment": new_review.comment,
            "rating": new_review.rating,
            "user_id": new_review.user_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# PUT - Atualizar uma avaliação
@bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Avaliação não encontrada"}), 404

    data = request.get_json()
    if "comment" in data:
        review.comment = data["comment"]
    if "rating" in data:
        review.rating = data["rating"]
    if "user_id" in data:
        review.user_id = data["user_id"]

    try:
        db.session.commit()
        return jsonify({
            "id": review.id,
            "comment": review.comment,
            "rating": review.rating,
            "user_id": review.user_id
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# DELETE - Remover uma avaliação
@bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Avaliação não encontrada"}), 404

    try:
        db.session.delete(review)
        db.session.commit()
        return jsonify({"message": "Avaliação removida com sucesso"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
