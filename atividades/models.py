from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    nota = db.Column(db.Float)  # Campo da nota adicionado
    turma_id = db.Column(db.Integer, nullable=False)
    professor_id = db.Column(db.Integer, nullable=False)
