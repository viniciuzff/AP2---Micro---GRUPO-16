from flask import Flask, request, jsonify
from flasgger import Swagger
from models import db, Professor, Turma, Aluno

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
swagger = Swagger(app)

# garante criação do DB compatível com Flask 3.x
with app.app_context():
    db.create_all()

# ---------------- Professores ----------------
@app.route('/professores', methods=['POST'])
def criar_professor():
    """
    Criar professor
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            nome:
              type: string
            idade:
              type: integer
            materia:
              type: string
            observacoes:
              type: string
    responses:
      201:
        description: Professor criado
    """
    data = request.get_json() or {}
    p = Professor(
        nome=data.get('nome'),
        idade=data.get('idade'),
        materia=data.get('materia'),
        observacoes=data.get('observacoes')
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({'id': p.id, 'nome': p.nome}), 201

@app.route('/professores', methods=['GET'])
def listar_professores():
    """
    Listar professores
    ---
    responses:
      200:
        description: Lista de professores
    """
    profs = Professor.query.all()
    return jsonify([{'id': p.id, 'nome': p.nome, 'idade': p.idade, 'materia': p.materia} for p in profs])

@app.route('/professores/<int:id>', methods=['PUT'])
def atualizar_professor(id):
    """
    Atualizar professor
    ---
    parameters:
      - in: path
        name: id
        required: true
        type: integer
      - in: body
        name: body
        schema:
          properties:
            nome: { type: string }
            idade: { type: integer }
            materia: { type: string }
            observacoes: { type: string }
    responses:
      200:
        description: Atualizado
    """
    p = Professor.query.get_or_404(id)
    data = request.get_json() or {}
    p.nome = data.get('nome', p.nome)
    p.idade = data.get('idade', p.idade)
    p.materia = data.get('materia', p.materia)
    p.observacoes = data.get('observacoes', p.observacoes)
    db.session.commit()
    return jsonify({'message': 'Professor atualizado'})

@app.route('/professores/<int:id>', methods=['DELETE'])
def deletar_professor(id):
    """
    Deletar professor
    ---
    parameters:
      - in: path
        name: id
        required: true
    """
    p = Professor.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': 'Professor deletado'})

# ---------------- Turmas ----------------
@app.route('/turmas', methods=['POST'])
def criar_turma():
    """
    Criar turma
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            descricao:
              type: string
            professor_id:
              type: integer
            ativo:
              type: boolean
    responses:
      201:
        description: Turma criada
    """
    data = request.get_json() or {}
    t = Turma(descricao=data.get('descricao'), professor_id=data.get('professor_id'), ativo=data.get('ativo', True))
    db.session.add(t)
    db.session.commit()
    return jsonify({'id': t.id, 'descricao': t.descricao}), 201

@app.route('/turmas', methods=['GET'])
def listar_turmas():
    """
    Listar turmas
    ---
    responses:
      200:
        description: Lista de turmas
    """
    turmas = Turma.query.all()
    return jsonify([{'id': t.id, 'descricao': t.descricao, 'professor_id': t.professor_id, 'ativo': t.ativo} for t in turmas])

@app.route('/turmas/<int:id>', methods=['PUT'])
def atualizar_turma(id):
    """
    Atualizar turma
    ---
    parameters:
      - in: path
        name: id
        required: true
      - in: body
        name: body
    responses:
      200:
        description: Atualizada
    """
    t = Turma.query.get_or_404(id)
    data = request.get_json() or {}
    t.descricao = data.get('descricao', t.descricao)
    t.professor_id = data.get('professor_id', t.professor_id)
    t.ativo = data.get('ativo', t.ativo)
    db.session.commit()
    return jsonify({'message': 'Turma atualizada'})

@app.route('/turmas/<int:id>', methods=['DELETE'])
def deletar_turma(id):
    """
    Deletar turma
    ---
    parameters:
      - in: path
        name: id
        required: true
    """
    t = Turma.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'Turma deletada'})

# ---------------- Alunos ----------------
@app.route('/alunos', methods=['POST'])
def criar_aluno():
    """
    Criar aluno
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            nome: { type: string }
            idade: { type: integer }
            turma_id: { type: integer }
            data_nascimento: { type: string }
    responses:
      201:
        description: Aluno criado
    """
    data = request.get_json() or {}
    a = Aluno(nome=data.get('nome'), idade=data.get('idade'), turma_id=data.get('turma_id'), data_nascimento=data.get('data_nascimento'))
    db.session.add(a)
    db.session.commit()
    return jsonify({'id': a.id, 'nome': a.nome}), 201

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    """
    Listar alunos
    ---
    responses:
      200:
        description: Lista de alunos
    """
    alunos = Aluno.query.all()
    return jsonify([{'id': a.id, 'nome': a.nome, 'idade': a.idade, 'turma_id': a.turma_id} for a in alunos])

@app.route('/alunos/<int:id>', methods=['PUT'])
def atualizar_aluno(id):
    """
    Atualizar aluno
    ---
    parameters:
      - in: path
        name: id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          properties:
            nome:
              type: string
            idade:
              type: integer
            turma_id:
              type: integer
            data_nascimento:
              type: string
    responses:
      200:
        description: Aluno atualizado com sucesso
    """
    a = Aluno.query.get_or_404(id)
    data = request.get_json() or {}
    a.nome = data.get('nome', a.nome)
    a.idade = data.get('idade', a.idade)
    a.turma_id = data.get('turma_id', a.turma_id)
    a.data_nascimento = data.get('data_nascimento', a.data_nascimento)
    db.session.commit()
    return jsonify({'message': 'Aluno atualizado com sucesso'})


@app.route('/alunos/<int:id>', methods=['DELETE'])
def deletar_aluno(id):
    """
    Deletar aluno
    ---
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
      200:
        description: Aluno deletado com sucesso
    """
    a = Aluno.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    return jsonify({'message': 'Aluno deletado com sucesso'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
