from flask import Flask, request, jsonify
from flasgger import Swagger
from models import db, Atividade
import requests
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atividades.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
swagger = Swagger(app)

# cria o banco automaticamente
with app.app_context():
    db.create_all()

# URL do microsserviço de gerenciamento (dinâmico)
MANAGEMENT_URL = os.getenv("MANAGEMENT_URL", "http://127.0.0.1:5000")

@app.route('/atividades', methods=['POST'])
def criar_atividade():
    """
    Criar atividade
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            descricao:
              type: string
            nota:
              type: number
            turma_id:
              type: integer
            professor_id:
              type: integer
    responses:
      201:
        description: Atividade criada
    """
    data = request.get_json()
    turma_id = data.get("turma_id")
    professor_id = data.get("professor_id")

    # valida IDs no microsserviço de gerenciamento
    try:
        resp_turmas = requests.get(f"{MANAGEMENT_URL}/turmas")
        resp_prof = requests.get(f"{MANAGEMENT_URL}/professores")
        resp_turmas.raise_for_status()
        resp_prof.raise_for_status()

        turmas = resp_turmas.json()
        profs = resp_prof.json()

        if not any(t["id"] == turma_id for t in turmas):
            return jsonify({"error": f"Turma com ID {turma_id} não encontrada"}), 404
        if not any(p["id"] == professor_id for p in profs):
            return jsonify({"error": f"Professor com ID {professor_id} não encontrado"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro comunicação: {e}"}), 500

    atividade = Atividade(
        descricao=data["descricao"],
        nota=data["nota"],
        turma_id=turma_id,
        professor_id=professor_id
    )
    db.session.add(atividade)
    db.session.commit()
    return jsonify({"id": atividade.id, "descricao": atividade.descricao}), 201

@app.route('/atividades', methods=['GET'])
def listar_atividades():
    """
    Listar atividades
    ---
    responses:
      200:
        description: Lista de atividades
    """
    atividades = Atividade.query.all()
    return jsonify([
        {"id": a.id, "descricao": a.descricao, "nota": a.nota, "turma_id": a.turma_id, "professor_id": a.professor_id}
        for a in atividades
    ])

@app.route('/atividades/<int:id>', methods=['DELETE'])
def deletar_atividade(id):
    """
    Deletar atividade
    ---
    parameters:
      - in: path
        name: id
        required: true
    """
    a = Atividade.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    return jsonify({"message": "Atividade deletada"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
