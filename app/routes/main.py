from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return {"message": "Salve! Vc acabou de entrar no primeiro APP do EVANDRO COSTA!"}
