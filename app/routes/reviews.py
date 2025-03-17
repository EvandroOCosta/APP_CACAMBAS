from flask import Blueprint

bp = Blueprint('reviews', __name__)

@bp.route('/reviews', methods=['GET'])
def get_reviews():
    return {"message": "Rota de avaliacoes funcionando!"}
