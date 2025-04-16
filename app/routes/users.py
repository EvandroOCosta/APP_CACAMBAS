#routes/users.py
from flask import Blueprint, request, jsonify
from config.database import db
from app.models.user import User
from app.schemas.user_schema import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('users', __name__)
user_schema = UserSchema()
user_schema_many = UserSchema(many=True)

# GET - Listar todos os usuários
@bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify(user_schema_many.dump(users))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST - Criar novo usuário
@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Validação com Marshmallow
    errors = user_schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400

    # Verifica se e-mail já existe
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "E-mail já cadastrado."}), 400

    hashed_password = generate_password_hash(data["password"])

    new_user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuário criado com sucesso!", "user": user_schema.dump(new_user)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# GET - Buscar usuário por ID
@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify(user_schema.dump(user))

# PUT - Atualizar usuário
@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    data = request.get_json()

    if "email" in data:
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"error": "E-mail já cadastrado por outro usuário."}), 400

    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = generate_password_hash(data["password"])

    try:
        db.session.commit()
        return jsonify({"message": "Usuário atualizado com sucesso!", "user": user_schema.dump(user)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# DELETE - Remover usuário
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
