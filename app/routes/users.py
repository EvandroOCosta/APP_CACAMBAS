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
