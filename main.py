from flask import Flask, render_template, request, flash, session, redirect, url_for, send_file
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from models import db, Usuario
from file_manager import UserFile, UserFolder, create_user_folder
from routes.user import user_bp
import os

print("INICIO DO ARQUIVO")  # 👈 teste

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = None 
app.secret_key= 'pinto123'


os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)

db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        action = request.form.get("action")
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if action == 'login':
            user = Usuario.query.filter_by(usuario=usuario).first()
            if not user:
                flash ('Usuário não encontrado.')
                return redirect(url_for("auth"))
            if not check_password_hash(user.senha, senha):
                flash ('Senha incorreta.')
                return redirect(url_for("auth"))
            
            session['user_id'] = user.id
            session['usuario'] = user.usuario
            return redirect(url_for("home"))
            
        elif action == 'register':
            usuario_existente = Usuario.query.filter_by(usuario=usuario).first()
            if usuario_existente:
                flash ('Usuário já existe. Escolha outro nome.')
                return redirect(url_for("auth"))

            if Usuario.query.filter_by(usuario=usuario).first():
                flash ('Usuário já existe. Escolha outro nome.')
            else:
                senha_hash = generate_password_hash(senha)
                novo = Usuario(usuario=usuario, senha=senha_hash)
                db.session.add(novo)
                db.session.commit()
                flash ('Usuário registrado com sucesso!')
    return render_template("auth.html")


@app.route("/home", methods=["GET", "POST"])
@app.route("/home/", methods=["GET", "POST"])
@app.route("/home/<path:folder_path>", methods=["GET", "POST"])
def home(folder_path=''):
    if 'user_id' not in session:
        return redirect(url_for("auth"))
    
    user = Usuario.query.get(session['user_id'])
    
    if request.method == "POST":
        action = request.form.get('action')
        
        if action == 'create_folder':
            folder_name = request.form.get('folder_name')
            if folder_name:
                # Criar pasta no sistema de arquivos
                user_folder = create_user_folder(user.id)
                full_folder_path = os.path.join(user_folder, folder_path, folder_name) if folder_path else os.path.join(user_folder, folder_name)
                os.makedirs(full_folder_path, exist_ok=True)
                
                # Salvar no banco
                db_folder_path = f"{folder_path}/{folder_name}" if folder_path else folder_name
                user_folder_db = UserFolder(
                    user_id=user.id,
                    folder_name=folder_name,
                    folder_path=db_folder_path,
                    parent_path=folder_path
                )
                db.session.add(user_folder_db)
                db.session.commit()
                flash('Pasta criada com sucesso!')
            
            if folder_path:
                return redirect(url_for('home', folder_path=folder_path))
            else:
                return redirect(url_for('home'))
        
        elif action == 'upload_file':
            if 'file' not in request.files:
                flash('Nenhum arquivo selecionado')
                if folder_path:
                    return redirect(url_for('home', folder_path=folder_path))
                else:
                    return redirect(url_for('home'))
            
            file = request.files['file']
            if file.filename == '':
                flash('Nenhum arquivo selecionado')
                if folder_path:
                    return redirect(url_for('home', folder_path=folder_path))
                else:
                    return redirect(url_for('home'))
            
            if file:
                # Criar pasta do usuário
                user_folder = create_user_folder(user.id)
                
                # Salvar arquivo na pasta correta
                filename = secure_filename(file.filename)
                unique_filename = f"{user.id}_{filename}"
                
                if folder_path:
                    file_dir = os.path.join(user_folder, folder_path)
                    os.makedirs(file_dir, exist_ok=True)
                    file_path = os.path.join(file_dir, unique_filename)
                else:
                    file_path = os.path.join(user_folder, unique_filename)
                
                file.save(file_path)
                
                # Salvar no banco
                user_file = UserFile(
                    user_id=user.id,
                    filename=unique_filename,
                    original_filename=filename,
                    file_path=file_path,
                    file_size=os.path.getsize(file_path),
                    file_type=filename.split('.')[-1] if '.' in filename else 'unknown',
                    folder_path=folder_path
                )
                db.session.add(user_file)
                db.session.commit()
                
                flash('Arquivo enviado com sucesso!')
                if folder_path:
                    return redirect(url_for('home', folder_path=folder_path))
                else:
                    return redirect(url_for('home'))
    
    # Buscar pastas e arquivos da pasta atual
    folders = UserFolder.query.filter_by(user_id=user.id, parent_path=folder_path).all()
    files = UserFile.query.filter_by(user_id=user.id, folder_path=folder_path).order_by(UserFile.upload_date.desc()).all()
    
    # Criar breadcrumb
    breadcrumb = []
    if folder_path:
        parts = folder_path.split('/')
        current_path = ''
        for part in parts:
            if part:  # Ignorar partes vazias
                current_path = f"{current_path}/{part}" if current_path else part
                breadcrumb.append({'name': part, 'path': current_path})
    
    return render_template("home.html", usuario=user, files=files, folders=folders, current_folder=folder_path, breadcrumb=breadcrumb)

@app.route("/download/<int:file_id>")
def download_file(file_id):
    if 'user_id' not in session:
        return redirect(url_for("auth"))
    
    user_file = UserFile.query.filter_by(id=file_id, user_id=session['user_id']).first()
    if not user_file:
        flash('Arquivo não encontrado')
        return redirect(url_for('home'))
    
    return send_file(user_file.file_path, as_attachment=True, download_name=user_file.original_filename)

@app.route("/delete/<int:file_id>")
def delete_file(file_id):
    if 'user_id' not in session:
        return redirect(url_for("auth"))
    
    user_file = UserFile.query.filter_by(id=file_id, user_id=session['user_id']).first()
    if not user_file:
        flash('Arquivo não encontrado')
        return redirect(url_for('home'))
    
    folder_path = user_file.folder_path
    
    # Deletar arquivo físico
    if os.path.exists(user_file.file_path):
        os.remove(user_file.file_path)
    
    # Deletar do banco
    db.session.delete(user_file)
    db.session.commit()
    
    flash('Arquivo deletado com sucesso!')
    if folder_path:
        return redirect(url_for('home', folder_path=folder_path))
    else:
        return redirect(url_for('home'))

@app.route("/delete_folder/<int:folder_id>")
def delete_folder(folder_id):
    if 'user_id' not in session:
        return redirect(url_for("auth"))
    
    folder = UserFolder.query.filter_by(id=folder_id, user_id=session['user_id']).first()
    if not folder:
        flash('Pasta não encontrada')
        return redirect(url_for('home'))
    
    parent_path = folder.parent_path
    
    # Deletar arquivos da pasta
    files_in_folder = UserFile.query.filter(UserFile.user_id == session['user_id'], 
                                           UserFile.folder_path.like(f"{folder.folder_path}%")).all()
    for file in files_in_folder:
        if os.path.exists(file.file_path):
            os.remove(file.file_path)
        db.session.delete(file)
    
    # Deletar subpastas
    subfolders = UserFolder.query.filter(UserFolder.user_id == session['user_id'],
                                        UserFolder.folder_path.like(f"{folder.folder_path}%")).all()
    for subfolder in subfolders:
        db.session.delete(subfolder)
    
    # Deletar pasta física
    user_folder = create_user_folder(session['user_id'])
    folder_physical_path = os.path.join(user_folder, folder.folder_path)
    if os.path.exists(folder_physical_path):
        import shutil
        shutil.rmtree(folder_physical_path)
    
    db.session.commit()
    flash('Pasta deletada com sucesso!')
    
    if parent_path:
        return redirect(url_for('home', folder_path=parent_path))
    else:
        return redirect(url_for('home'))

@app.route("/preview/<int:file_id>")
def preview_file(file_id):
    if 'user_id' not in session:
        return redirect(url_for("auth"))
    
    user_file = UserFile.query.filter_by(id=file_id, user_id=session['user_id']).first()
    if not user_file:
        flash('Arquivo não encontrado')
        return redirect(url_for('home'))
    
    return send_file(user_file.file_path)

#register blueprints
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == "__main__":
    print("CRIANDO BANCO")  # 👈 teste
    with app.app_context():
        db.create_all()
    print("BANCO CRIADO")  # 👈 teste
    app.run(debug=True, host='0.0.0.0', port=5000)