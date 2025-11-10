from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.String(50))
    lab = db.Column(db.Boolean, default=False)
    data = db.Column(db.String(20))
    turma_id = db.Column(db.Integer, nullable=False)
