from models import db
from datetime import datetime
import os

class UserFile(db.Model):
    __tablename__ = 'user_files'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_type = db.Column(db.String(50))
    folder_path = db.Column(db.String(500), default='')

class UserFolder(db.Model):
    __tablename__ = 'user_folders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    folder_name = db.Column(db.String(255), nullable=False)
    folder_path = db.Column(db.String(500), nullable=False)
    parent_path = db.Column(db.String(500), default='')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

def create_user_folder(user_id):
    """Cria pasta específica para o usuário"""
    user_folder = f"user_files/{user_id}"
    os.makedirs(user_folder, exist_ok=True)
    return user_folder