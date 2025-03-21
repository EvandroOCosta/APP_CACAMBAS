from flask import Blueprint, request, jsonify
from config.database import db
from app.models.user import User

bp = Blueprint('users', __name__)

# Rota para listar usuários
@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    
    return jsonify(users_list)
