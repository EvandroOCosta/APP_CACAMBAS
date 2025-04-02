from flask import Blueprint, request, jsonify
from config.database import db
from app.models.dumpster import Dumpster


bp = Blueprint('dumpsters', __name__)

# 🟢 GET - Listar todas as caçambas
@bp.route('/dumpsters', methods=['GET'])
def get_dumpsters():
    try:
        dumpsters = Dumpster.query.all()
        return jsonify([{"id": d.id, "location": d.location, "size": d.size} for d in dumpsters])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

# 🟢 POST - Criar uma nova caçamba
@bp.route('/dumpsters', methods=['POST'])
def create_dumpster():
    data = request.get_json()
    if not data or not all(key in data for key in ["location", "size"]):
        return jsonify({"error": "Os campos 'location' e 'size' são obrigatórios."}), 400

    new_dumpster = Dumpster(location=data["location"], size=data["size"])
    try:
        db.session.add(new_dumpster)
        db.session.commit()
        return jsonify({"message": "Caçamba criada com sucesso!", "dumpster": {"id": new_dumpster.id, "location": new_dumpster.location, "size": new_dumpster.size}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

# 🟢 GET - Buscar uma caçamba específica
@bp.route('/dumpsters/<int:id>', methods=['GET'])
def get_dumpster(id):
    dumpster = Dumpster.query.get(id)
    if not dumpster:
        return jsonify({"error": "Caçamba não encontrada"}), 404
    return jsonify({"id": dumpster.id, "location": dumpster.location, "size": dumpster.size})

# 🟢 PUT - Atualizar uma caçamba
@bp.route('/dumpsters/<int:id>', methods=['PUT'])
def update_dumpster(id):
    dumpster = Dumpster.query.get(id)
    if not dumpster:
        return jsonify({"error": "Caçamba não encontrada"}), 404

    data = request.get_json()
    if "location" in data:
        dumpster.location = data["location"]
    if "size" in data:
        dumpster.size = data["size"]

    try:
        db.session.commit()
        return jsonify({"message": "Caçamba atualizada com sucesso!", "dumpster": {"id": dumpster.id, "location": dumpster.location, "size": dumpster.size}}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

# 🟢 DELETE - Remover uma caçamba
@bp.route('/dumpsters/<int:id>', methods=['DELETE'])
def delete_dumpster(id):
    dumpster = Dumpster.query.get(id)
    if not dumpster:
        return jsonify({"error": "Caçamba não encontrada"}), 404

    try:
        db.session.delete(dumpster)
        db.session.commit()
        return jsonify({"message": "Caçamba removida com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()
