from flask import Blueprint

bp = Blueprint('users', __name__)

@bp.route('/users', methods=['GET'])
def get_users():
    return {"message": "Rota de usuarios funcionando!"}
