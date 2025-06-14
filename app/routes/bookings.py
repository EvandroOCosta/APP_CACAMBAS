# app/routes/bookings.py
from flask import Blueprint, request, jsonify
from app.models.booking import Booking
from config.database import db

bp = Blueprint('bookings', __name__)

# POST - Criar uma nova reserva
@bp.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()

    # Verifica se todos os campos obrigatórios foram fornecidos
    required_fields = ["user_id", "dumpster_id", "start_date", "end_date"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Campos obrigatórios: user_id, dumpster_id, start_date, end_date"}), 400

    try:
        booking = Booking(
            user_id=data["user_id"],
            dumpster_id=data["dumpster_id"],
            start_date=data["start_date"],
            end_date=data["end_date"]
        )
        db.session.add(booking)
        db.session.commit()
        return jsonify(booking.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.session.close()


# GET - Listar todas as reservas
@bp.route('/bookings', methods=['GET'])
def get_bookings():
    try:
        bookings = Booking.query.all()
        return jsonify([b.to_dict() for b in bookings]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        db.session.close()


# GET - Buscar uma reserva por ID
@bp.route('/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    try:
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({"error": "Reserva não encontrada"}), 404
        return jsonify(booking.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        db.session.close()


# PUT - Atualizar uma reserva
@bp.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Reserva não encontrada"}), 404

    data = request.get_json()

    try:
        booking.user_id = data.get("user_id", booking.user_id)
        booking.dumpster_id = data.get("dumpster_id", booking.dumpster_id)
        booking.start_date = data.get("start_date", booking.start_date)
        booking.end_date = data.get("end_date", booking.end_date)

        db.session.commit()
        return jsonify(booking.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.session.close()


# DELETE - Deletar uma reserva
@bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Reserva não encontrada"}), 404

    try:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({"message": "Reserva deletada com sucesso"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.session.close()
