from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100),unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    imagem_perfil = db.Column(db.String(200), default='default.png')