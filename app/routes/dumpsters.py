from flask import Blueprint

bp = Blueprint('dumpsters', __name__)

@bp.route('/dumpsters', methods=['GET'])
def get_dumpsters():
    return {"message": "Rota de cacambas funcionando!"}
