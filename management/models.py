from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    materia = db.Column(db.String(100))
    observacoes = db.Column(db.Text)

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, nullable=False)
    ativo = db.Column(db.Boolean, default=True)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    turma_id = db.Column(db.Integer)
    data_nascimento = db.Column(db.String(10))
