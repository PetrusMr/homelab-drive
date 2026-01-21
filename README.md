# 🏠 Homelab Drive

Um sistema de armazenamento de arquivos pessoal desenvolvido em Python/Flask para uso doméstico. Permite que múltiplos usuários gerenciem seus arquivos de forma segura e organizada.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![Mobile](https://img.shields.io/badge/Mobile-Friendly-orange.svg)

## 📸 Screenshots

### Interface Desktop


### Interface Mobile


## ✨ Funcionalidades

### 🔐 Autenticação
- Sistema de login/registro seguro
- Hash de senhas com Werkzeug
- Sessões isoladas por usuário

### 📁 Gerenciamento de Arquivos
- Upload de arquivos sem limite de tamanho
- Organização em pastas e subpastas
- Preview de imagens, PDFs e documentos
- Download de arquivos
- Exclusão de arquivos e pastas

### 👤 Perfil de Usuário
- Foto de perfil personalizável
- Editor de imagem com zoom/rotação/posicionamento
- Alteração de nome de usuário e senha
- Logout seguro

### 📱 Interface Responsiva
- Design adaptável para mobile
- Touch-friendly para dispositivos móveis
- Navegação intuitiva com breadcrumb

### 🔒 Segurança
- Isolamento total entre usuários
- Validação de tipos de arquivo
- Proteção contra acesso não autorizado
- Sanitização de nomes de arquivo

## 🛠️ Stack Tecnológica

- **Backend**: Python 3.8+ com Flask
- **Banco de Dados**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Autenticação**: Flask-Session + Werkzeug
- **ORM**: SQLAlchemy
- **Upload**: Werkzeug FileStorage
- **Processamento de Imagem**: Pillow

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Ubuntu Server (recomendado) ou qualquer sistema Linux
- 1GB+ de RAM
- Espaço em disco conforme necessário

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/homelab-drive.git
cd homelab-drive
```

### 2. Crie ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco
```bash
python3 -c "from main import app, db; app.app_context().push(); db.create_all()"
```

### 5. Execute a aplicação
```bash
python3 main.py
```

### 6. Acesse no navegador
```
http://localhost:5000
```

## 🐳 Deploy com Docker (Opcional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python3", "main.py"]
```

```bash
docker build -t homelab-drive .
docker run -p 5000:5000 -v $(pwd)/user_files:/app/user_files homelab-drive
```

## 📁 Estrutura do Projeto

```
homelab-drive/
├── main.py                 # Aplicação principal
├── models.py              # Modelos do banco de dados
├── file_manager.py        # Gerenciamento de arquivos
├── routes/
│   └── user.py           # Rotas de usuário
├── templates/
│   ├── auth.html         # Página de login/registro
│   ├── home.html         # Interface principal
│   ├── perfil.html       # Página de perfil
│   └── editar_perfil.html # Edição de perfil
├── static/
│   ├── css/
│   │   └── style.css     # Estilos CSS
│   ├── js/
│   │   ├── script.js     # Scripts gerais
│   │   └── image-editor.js # Editor de imagem
│   ├── image/            # Imagens do sistema
│   └── uploads/          # Fotos de perfil
├── user_files/           # Arquivos dos usuários
├── instance/
│   └── usuarios.db       # Banco SQLite
└── requirements.txt      # Dependências Python
```

## 🔧 Configuração

### Variáveis de Ambiente
```bash
export FLASK_ENV=production
export SECRET_KEY=sua-chave-secreta-aqui
```

### Configurações no main.py
```python
app.config['MAX_CONTENT_LENGTH'] = None  # Sem limite de upload
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'sua-chave-secreta'  # MUDE EM PRODUÇÃO!
```

## 📱 Uso

1. **Registro**: Crie uma conta na página inicial
2. **Login**: Acesse com suas credenciais
3. **Upload**: Envie arquivos usando o formulário
4. **Organização**: Crie pastas para organizar arquivos
5. **Navegação**: Use o breadcrumb para navegar
6. **Preview**: Visualize imagens e documentos
7. **Perfil**: Personalize sua foto e dados

## 🔒 Segurança

### Implementado
- ✅ Hash de senhas
- ✅ Validação de sessões
- ✅ Isolamento entre usuários
- ✅ Sanitização de arquivos
- ✅ Proteção CSRF básica

### Recomendações para Produção
- [ ] HTTPS com certificado SSL
- [ ] Rate limiting
- [ ] Backup automático
- [ ] Monitoramento de logs
- [ ] Firewall configurado

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Roadmap

- [ ] Compartilhamento de arquivos entre usuários
- [ ] Versionamento de arquivos
- [ ] Sincronização com apps mobile
- [ ] API REST
- [ ] Integração com serviços de nuvem
- [ ] Sistema de backup automático
- [ ] Logs de auditoria
- [ ] Suporte a temas

## 🐛 Problemas Conhecidos

- Upload de arquivos muito grandes pode ser lento
- Preview limitado a alguns tipos de arquivo
- Sem suporte a edição online de documentos


## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@PetrusMR](https://github.com/PetrusMR)
- LinkedIn: [Petrusl](https://www.linkedin.com/in/petrus-machado-372a8234b/)

## 🙏 Agradecimentos

- Comunidade Flask pela documentação
- Stack Overflow pelas soluções
- Família pelo apoio durante o desenvolvimento

---

⭐ Se este projeto te ajudou, deixe uma estrela!

## 📊 Status do Projeto

![GitHub last commit](https://img.shields.io/github/last-commit/PetrusMR/homelab-drive)
![GitHub issues](https://img.shields.io/github/issues/PetrusMR/homelab-drive)
![GitHub stars](https://img.shields.io/github/stars/PetrusMR/homelab-drive)