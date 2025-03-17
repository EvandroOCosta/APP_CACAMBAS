from flask import Blueprint

bp = Blueprint('bookings', __name__)

@bp.route('/bookings', methods=['GET'])
def get_bookings():
    return {"message": "Rota de reservas funcionando!"}
