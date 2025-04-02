from flask import Blueprint, request, jsonify
from config.database import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('users', __name__)

# Rota para listar usuários
@bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para criar um usuário
@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Validação de campos obrigatórios e vazios
    if not data or not all(key in data for key in ["name", "email", "password"]):
        return jsonify({"error": "Os campos 'name', 'email' e 'password' são obrigatórios."}), 400

    if not data["name"].strip() or not data["email"].strip() or not data["password"].strip():
        return jsonify({"error": "Todos os campos devem ser preenchidos."}), 400

    # Verifica se o e-mail já está cadastrado
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"error": "E-mail já cadastrado."}), 400

    # Criptografa a senha antes de salvar
    hashed_password = generate_password_hash(data["password"])

    new_user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuário criado com sucesso!", "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Rota para buscar um usuário por ID
@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email
    })

# Rota para atualizar um usuário
@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    data = request.get_json()

    if "name" in data and data["name"].strip():
        user.name = data["name"]
    if "email" in data and data["email"].strip():
        # Verifica se o e-mail já está sendo usado por outro usuário
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"error": "E-mail já cadastrado por outro usuário."}), 400
        user.email = data["email"]
    if "password" in data and data["password"].strip():
        user.password = generate_password_hash(data["password"])

    try:
        db.session.commit()
        return jsonify({"message": "Usuário atualizado com sucesso!", "user": {"id": user.id, "name": user.name, "email": user.email}}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Rota para deletar um usuário
@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuário deletado com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
