from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import math
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///desafio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)
Session(app)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    nascimento = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # normal or admin

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Divida(db.Model):
    __tablename__ = 'divida'
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    data_vencimento = db.Column(db.String(10), nullable=False)
    cpf_usuario = db.Column(db.String(11), db.ForeignKey('usuario.cpf'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    cpf = data['cpf']
    nome = data['nome']
    nascimento = data['nascimento']
    email = data['email']
    senha = data['senha']
    tipo_usuario = 'admin' if email.endswith('@br.dominiox.com') else 'normal'

    if Usuario.query.filter_by(cpf=cpf).first() or Usuario.query.filter_by(email=email).first():
        return jsonify({'mensagem': 'Usuário já existe'}), 400

    novo_usuario = Usuario(cpf=cpf, nome=nome, nascimento=nascimento, email=email, tipo=tipo_usuario)
    novo_usuario.set_senha(senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário cadastrado com sucesso'}), 201

@app.route('/entrar', methods=['POST'])
def entrar():
    data = request.get_json()
    cpf = data['cpf']
    senha = data['senha']

    usuario = Usuario.query.filter_by(cpf=cpf).first()
    if usuario and usuario.check_senha(senha):
        session['cpf_usuario'] = usuario.cpf
        session['tipo_usuario'] = usuario.tipo
        return jsonify({'mensagem': 'Login realizado com sucesso'}), 200

    return jsonify({'mensagem': 'Credenciais inválidas'}), 401

@app.route('/sair', methods=['POST'])
def sair():
    session.pop('cpf_usuario', None)
    session.pop('tipo_usuario', None)
    return jsonify({'mensagem': 'Logout realizado com sucesso'}), 200

def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'cpf_usuario' not in session:
            return jsonify({'mensagem': 'Login requerido'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/dividas', methods=['GET'])
@login_requerido
def obter_dividas():
    cpf_usuario = session['cpf_usuario']
    dividas = Divida.query.filter_by(cpf_usuario=cpf_usuario).all()
    return jsonify([{'valor': divida.valor, 'data_vencimento': divida.data_vencimento} for divida in dividas]), 200

@app.route('/dividas', methods=['POST'])
@login_requerido
def adicionar_divida():
    if session.get('tipo_usuario') != 'admin':
        return jsonify({'mensagem': 'Acesso de administrador requerido'}), 403

    data = request.get_json()
    valor = data['valor']
    data_vencimento = data['data_vencimento']
    cpf_usuario = data['cpf_usuario']

    nova_divida = Divida(valor=valor, data_vencimento=data_vencimento, cpf_usuario=cpf_usuario)
    db.session.add(nova_divida)
    db.session.commit()

    return jsonify({'mensagem': 'Dívida adicionada com sucesso'}), 201

@app.route('/score', methods=['GET'])
@login_requerido
def obter_score():
    cpf_usuario = session['cpf_usuario']
    dividas = Divida.query.filter_by(cpf_usuario=cpf_usuario).all()
    if not dividas:
        return jsonify({'score': 1000}), 200  # Sem dívidas significa pontuação perfeita

    valor_medio_dividas = sum(divida.valor for divida in dividas) / len(dividas)
    score = 1000 * math.exp(-math.sqrt(valor_medio_dividas))
    return jsonify({'score': score}), 200

if __name__ == '__main__':
    app.run(debug=True)
