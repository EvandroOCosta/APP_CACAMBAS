from flask import Blueprint, request, jsonify
from config.database import db
from app.models.user import User

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
    finally:
        db.session.close()  # Garante que a sessão do banco de dados seja fechada corretamente

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()  # Recebe os dados do corpo da requisição

    # Validação básica
    if not data or not all(key in data for key in ["name", "email", "password"]):
        return jsonify({"error": "Dados inválidos. Os campos 'name', 'email' e 'password' são obrigatórios."}), 400

    # Criar novo usuário
    new_user = User(
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuário criado com sucesso!", "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)  # Busca o usuário pelo ID

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email
    })

@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)  # Busca o usuário pelo ID

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    data = request.get_json()  # Recebe os novos dados

    # Atualiza apenas os campos enviados na requisição
    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = data["password"]

    try:
        db.session.commit()
        return jsonify({
            "message": "Usuário atualizado com sucesso!",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)  # Busca o usuário pelo ID

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuário deletado com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()
