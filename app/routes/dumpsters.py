#routes/dumpsters.py

from flask import Blueprint, request, jsonify
from config.database import db
from app.models.dumpster import Dumpster
from app.schemas.dumpsters_schema import DumpsterSchema

bp = Blueprint('dumpsters', __name__)
schema = DumpsterSchema()
schema_many = DumpsterSchema(many=True)

# GET - Listar todas as caçambas
@bp.route('/dumpsters', methods=['GET'])
def get_dumpsters():
    try:
        dumpsters = Dumpster.query.all()
        return jsonify(schema_many.dump(dumpsters)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

# POST - Criar nova caçamba com validação
@bp.route('/dumpsters', methods=['POST'])
def create_dumpster():
    data = request.get_json()
    errors = schema.validate(data)

    if errors:
        return jsonify({"error": errors}), 400

    new_dumpster = Dumpster(location=data["location"], size=data["size"])
    try:
        db.session.add(new_dumpster)
        db.session.commit()
        return jsonify({"message": "Caçamba criada com sucesso!", "dumpster": schema.dump(new_dumpster)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

# GET - Obter caçamba por ID
@bp.route('/dumpsters/<int:id>', methods=['GET'])
def get_dumpster(id):
    dumpster = Dumpster.query.get(id)
    if not dumpster:
        return jsonify({"error": "Caçamba não encontrada"}), 404
    return jsonify(schema.dump(dumpster)), 200

# PUT - Atualizar caçamba
@bp.route('/dumpsters/<int:id>', methods=['PUT'])
def update_dumpster(id):
    dumpster = Dumpster.query.get(id)
    if not dumpster:
        return jsonify({"error": "Caçamba não encontrada"}), 404

    data = request.get_json()
    errors = schema.validate(data, partial=True)

    if errors:
        return jsonify({"error": errors}), 400

    if "location" in data:
        dumpster.location = data["location"]
    if "size" in data:
        dumpster.size = data["size"]

    try:
        db.session.commit()
        return jsonify({"message": "Caçamba atualizada com sucesso!", "dumpster": schema.dump(dumpster)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

# DELETE - Remover caçamba
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

