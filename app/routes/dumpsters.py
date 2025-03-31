from flask import Blueprint, request, jsonify

bp = Blueprint('dumpsters', __name__)

# Simulação de banco de dados em memória
dumpsters = [
    {"id": 1, "location": "Rua A, 123", "size": "5m³"},
    {"id": 2, "location": "Av. B, 456", "size": "7m³"}
]

# 🟢 GET - Listar todas as caçambas
@bp.route('/dumpsters', methods=['GET'])
def get_dumpsters():
    return jsonify(dumpsters)

# 🟢 POST - Criar uma nova caçamba
@bp.route('/dumpsters', methods=['POST'])
def create_dumpster():
    data = request.get_json()
    new_id = max(d['id'] for d in dumpsters) + 1 if dumpsters else 1
    new_dumpster = {"id": new_id, "location": data["location"], "size": data["size"]}
    dumpsters.append(new_dumpster)
    return jsonify(new_dumpster), 201

# 🟢 GET - Buscar uma caçamba específica
@bp.route('/dumpsters/<int:id>', methods=['GET'])
def get_dumpster(id):
    dumpster = next((d for d in dumpsters if d["id"] == id), None)
    if not dumpster:
        return jsonify({"error": "Caçamba não encontrada"}), 404
    return jsonify(dumpster)

# 🟢 PUT - Atualizar uma caçamba
@bp.route('/dumpsters/<int:id>', methods=['PUT'])
def update_dumpster(id):
    data = request.get_json()
    dumpster = next((d for d in dumpsters if d["id"] == id), None)
    if not dumpster:
        return jsonify({"error": "Caçamba não encontrada"}), 404
    dumpster.update({"location": data.get("location", dumpster["location"]),
                     "size": data.get("size", dumpster["size"])})
    return jsonify(dumpster)

# 🟢 DELETE - Remover uma caçamba
@bp.route('/dumpsters/<int:id>', methods=['DELETE'])
def delete_dumpster(id):
    global dumpsters
    dumpsters = [d for d in dumpsters if d["id"] != id]
    return jsonify({"message": "Caçamba removida com sucesso"}), 200
