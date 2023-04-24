from . import db
from flask_login import UserMixin


class Professor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    senha = db.Column(db.String(200), nullable=False)

    turmas = db.relationship("Turma", backref="professor", lazy=True)


class Estudante(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    senha = db.Column(db.String(200), nullable=False)

    matriculas = db.relationship("Matricula", backref="estudante", lazy=True)


class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(50), nullable=False)
    semestre = db.Column(db.String(10), nullable=False)

    professor_id = db.Column(db.Integer, db.ForeignKey(
        "professor.id"), nullable=False)
    matriculas = db.relationship("Matricula", backref="turma", lazy=True)


class Matricula(db.Model):
    estudante_id = db.Column(db.Integer, db.ForeignKey(
        "estudante.id"), primary_key=True)
    turma_id = db.Column(db.Integer, db.ForeignKey(
        "turma.id"), primary_key=True)


class Presenca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=True)

    matricula_estudante_id = db.Column(db.Integer, db.ForeignKey(
        "matricula.estudante_id"), nullable=False)
    matricula_turma_id = db.Column(db.Integer, db.ForeignKey(
        "matricula.turma_id"), nullable=False)
