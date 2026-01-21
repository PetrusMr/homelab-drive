from flask import Blueprint, render_template, session, redirect, url_for, request, flash, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario
import os
import base64
from PIL import Image
from io import BytesIO

user_bp = Blueprint('user', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image_data(image_data, user_id):
    """Processa dados base64 da imagem editada"""
    try:
        # Remover prefixo data:image
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Abrir imagem com PIL
        img = Image.open(BytesIO(image_bytes))
        
        # Salvar como JPEG
        filename = f"{user_id}_profile.jpg"
        file_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
        img.save(file_path, 'JPEG', quality=90)
        
        return filename
    except Exception as e:
        print(f"Erro ao processar imagem: {e}")
        return None

@user_bp.route("/", methods=["GET"])
def perfil():
    if 'user_id' in session:
        user = Usuario.query.get(session['user_id'])
        return render_template('perfil.html', usuario=user)
    return redirect(url_for('auth'))

@user_bp.route("/editar", methods=["GET", "POST"])
def editar_perfil():
    if 'user_id' not in session:
        return redirect(url_for('auth'))
    
    user = Usuario.query.get(session['user_id'])
    
    if request.method == "POST":
        novo_usuario = request.form.get('usuario')
        senha_atual = request.form.get('senha_atual')
        nova_senha = request.form.get('nova_senha')
        
        # Verificar se o novo nome de usuário já existe
        if novo_usuario != user.usuario:
            existing_user = Usuario.query.filter_by(usuario=novo_usuario).first()
            if existing_user:
                flash('Nome de usuário já existe!')
                return redirect(url_for('user.editar_perfil'))
        
        # Atualizar nome de usuário
        user.usuario = novo_usuario
        session['usuario'] = novo_usuario
        
        # Atualizar senha se fornecida
        if senha_atual and nova_senha:
            if check_password_hash(user.senha, senha_atual):
                user.senha = generate_password_hash(nova_senha)
            else:
                flash('Senha atual incorreta!')
                return redirect(url_for('user.editar_perfil'))
        
        # Upload de imagem
        image_data = request.form.get('image_data')
        if image_data:
            # Processar imagem editada
            filename = process_image_data(image_data, user.id)
            if filename:
                user.imagem_perfil = filename
        elif 'imagem' in request.files:
            # Upload tradicional (fallback)
            file = request.files['imagem']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"{user.id}_{file.filename}")
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(os.path.join(current_app.root_path, file_path))
                user.imagem_perfil = filename
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!')
        return redirect(url_for('user.perfil'))
    
    return render_template('editar_perfil.html', usuario=user)

@user_bp.route("/logout")
def logout():
    session.clear()
    flash('Logout realizado com sucesso!')
    return redirect(url_for('auth'))