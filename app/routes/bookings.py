from flask import Blueprint, request, jsonify

bp = Blueprint('bookings', __name__)

# Simulação de banco de dados
bookings_db = []
booking_id_counter = 1

# Criar uma reserva (POST)
@bp.route('/bookings', methods=['POST'])
def create_booking():
    global booking_id_counter
    data = request.get_json()
    new_booking = {
        "id": booking_id_counter,
        "user_id": data["user_id"],
        "dumpster_id": data["dumpster_id"],
        "start_date": data["start_date"],
        "end_date": data["end_date"]
    }
    bookings_db.append(new_booking)
    booking_id_counter += 1
    return jsonify(new_booking), 201

# Listar todas as reservas (GET)
@bp.route('/bookings', methods=['GET'])
def get_bookings():
    return jsonify(bookings_db), 200

# Obter uma reserva por ID (GET)
@bp.route('/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    for booking in bookings_db:
        if booking["id"] == booking_id:
            return jsonify(booking), 200
    return jsonify({"error": "Booking not found"}), 404

# Atualizar uma reserva por ID (PUT)
@bp.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    data = request.get_json()
    for booking in bookings_db:
        if booking["id"] == booking_id:
            booking["user_id"] = data.get("user_id", booking["user_id"])
            booking["dumpster_id"] = data.get("dumpster_id", booking["dumpster_id"])
            booking["start_date"] = data.get("start_date", booking["start_date"])
            booking["end_date"] = data.get("end_date", booking["end_date"])
            return jsonify(booking), 200
    return jsonify({"error": "Booking not found"}), 404

# Excluir uma reserva por ID (DELETE)
@bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    global bookings_db
    bookings_db = [booking for booking in bookings_db if booking["id"] != booking_id]
    return jsonify({"message": "Booking deleted"}), 200
