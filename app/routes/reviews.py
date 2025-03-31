from flask import Blueprint, request, jsonify
from schemas.review_schema import ReviewSchema  # Importando o esquema de validação

bp = Blueprint('reviews', __name__)

@bp.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()  # Obtendo os dados da requisição

    schema = ReviewSchema()  # Criando uma instância do esquema de validação
    errors = schema.validate(data)  # Validando os dados

    if errors:
        return jsonify({"errors": errors}), 400  # Retornando erros se houverem

    return jsonify({"message": "Review cadastrada com sucesso!", "data": data}), 201

# Simulação de banco de dados (lista)
reviews = []
review_id_counter = 1

# GET - Listar todas as avaliações
@bp.route('/reviews', methods=['GET'])
def get_reviews():
    return jsonify(reviews)

# POST - Criar uma nova avaliação
@bp.route('/reviews', methods=['POST'])
def create_review():
    global review_id_counter
    data = request.get_json()
    
    # Validação básica
    if not all(key in data for key in ["user_id", "dumpster_id", "rating", "comment"]):
        return jsonify({"error": "Campos obrigatórios: user_id, dumpster_id, rating, comment"}), 400
    
    new_review = {
        "id": review_id_counter,
        "user_id": data["user_id"],
        "dumpster_id": data["dumpster_id"],
        "rating": data["rating"],
        "comment": data["comment"]
    }
    reviews.append(new_review)
    review_id_counter += 1

    return jsonify(new_review), 201

# GET - Obter uma única avaliação por ID
@bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = next((r for r in reviews if r["id"] == review_id), None)
    if review:
        return jsonify(review)
    return jsonify({"error": "Avaliação não encontrada"}), 404

# PUT - Atualizar uma avaliação
@bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    review = next((r for r in reviews if r["id"] == review_id), None)

    if review:
        review.update({key: data[key] for key in data if key in review})
        return jsonify(review)
    
    return jsonify({"error": "Avaliação não encontrada"}), 404

# DELETE - Remover uma avaliação
@bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    global reviews
    reviews = [r for r in reviews if r["id"] != review_id]
    
    return jsonify({"message": "Avaliação removida com sucesso"}), 200
