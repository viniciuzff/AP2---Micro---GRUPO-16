from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reserva(db.Model):
    _tablename_ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.String(100), nullable=False)
    lab = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(20))
    turma_id = db.Column(db.Integer, nullable=False)