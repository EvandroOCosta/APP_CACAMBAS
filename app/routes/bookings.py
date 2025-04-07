# app/routes/bookings.py
from flask import Blueprint, request, jsonify
from app.models.booking import Booking
from config.database import db

bp = Blueprint('bookings', __name__)

@bp.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    booking = Booking(
        user_id=data["user_id"],
        dumpster_id=data["dumpster_id"],
        start_date=data["start_date"],
        end_date=data["end_date"]
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify(booking.to_dict()), 201

@bp.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([b.to_dict() for b in bookings]), 200

@bp.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking não encontrado"}), 404

    data = request.get_json()
    booking.user_id = data.get("user_id", booking.user_id)
    booking.dumpster_id = data.get("dumpster_id", booking.dumpster_id)
    booking.start_date = data.get("start_date", booking.start_date)
    booking.end_date = data.get("end_date", booking.end_date)
    
    db.session.commit()
    return jsonify(booking.to_dict()), 200

@bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking não encontrado"}), 404

    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking deletado com sucesso"}), 200
