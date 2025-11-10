from flask import Flask, request, jsonify
from flasgger import Swagger
from models import db, Reserva
import requests
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
swagger = Swagger(app)

# cria o banco automaticamente
with app.app_context():
    db.create_all()

# URL do microsserviço de gerenciamento (dinâmico)
MANAGEMENT_URL = os.getenv("MANAGEMENT_URL", "http://127.0.0.1:5000")

@app.route('/reservas', methods=['POST'])
def criar_reserva():
    """
    Criar reserva
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            data:
              type: string
            sala:
              type: integer
            lab:
              type: boolean
            turma_id:
              type: integer
    responses:
      201:
        description: Reserva criada
    """
    data = request.get_json()
    turma_id = data.get("turma_id")

    # valida turma com o microsserviço de management
    try:
        resp = requests.get(f"{MANAGEMENT_URL}/turmas")
        resp.raise_for_status()
        turmas = resp.json()
        if not any(t["id"] == turma_id for t in turmas):
            return jsonify({"error": f"Turma com ID {turma_id} não encontrada"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro comunicação: {e}"}), 500

    # criar reserva com os nomes corretos do modelo
    reserva = Reserva(
        data=data["data"],
        num_sala=int(data["sala"]),
        lab=bool(data.get("lab", False)),
        turma_id=turma_id
    )

    db.session.add(reserva)
    db.session.commit()
    return jsonify({"id": reserva.id, "sala": reserva.num_sala, "lab": reserva.lab}), 201


@app.route('/reservas', methods=['GET'])
def listar_reservas():
    """
    Listar reservas
    ---
    responses:
      200:
        description: Lista de reservas
    """
    reservas = Reserva.query.all()
    return jsonify([
        {"id": r.id, "data": r.data, "sala": r.num_sala, "lab": r.lab, "turma_id": r.turma_id}
        for r in reservas
    ])


@app.route('/reservas/<int:id>', methods=['PUT'])
def atualizar_reserva(id):
    """
    Atualizar uma reserva existente
    ---
    parameters:
      - in: path
        name: id
        required: true
      - in: body
        name: body
        required: true
        schema:
          properties:
            data:
              type: string
            sala:
              type: integer
            lab:
              type: boolean
            turma_id:
              type: integer
    responses:
      200:
        description: Reserva atualizada
    """
    reserva = Reserva.query.get_or_404(id)
    data = request.get_json()

    if "data" in data:
        reserva.data = data["data"]
    if "sala" in data:
        reserva.num_sala = int(data["sala"])
    if "lab" in data:
        reserva.lab = bool(data["lab"])
    if "turma_id" in data:
        turma_id = data["turma_id"]
        try:
            resp = requests.get(f"{MANAGEMENT_URL}/turmas")
            resp.raise_for_status()
            turmas = resp.json()
            if not any(t["id"] == turma_id for t in turmas):
                return jsonify({"error": f"Turma com ID {turma_id} não encontrada"}), 404
            reserva.turma_id = turma_id
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Erro comunicação: {e}"}), 500

    db.session.commit()
    return jsonify({
        "message": "Reserva atualizada com sucesso",
        "reserva": {"id": reserva.id, "data": reserva.data, "sala": reserva.num_sala, "lab": reserva.lab, "turma_id": reserva.turma_id}
    })


@app.route('/reservas/<int:id>', methods=['DELETE'])
def deletar_reserva(id):
    """
    Deletar reserva
    ---
    parameters:
      - in: path
        name: id
        required: true
    """
    r = Reserva.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({"message": "Reserva deletada"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
