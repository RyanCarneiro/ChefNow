# Imports para Flask e funcionalidades básicas
import threading
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import sqlite3
import os
import hashlib
import jwt
from datetime import datetime, timedelta
from functools import wraps

# Imports para o chat Hugging Face
import requests

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Configuração da chave secreta para JWT e sessões
JWT_SECRET = 'qTLzPaVdyNjMPM+Z3d38N9hV0a3f0WeGblcPjJTA6UOmujDsXxgFcDhF6F1k9x7A2cUzIatMQ//m8zBQ64YuvNWZQkz9k7B2vSxez8yt8DJsdUbFZzG6zU2TAarAiM/h5bcXnlmHe9VwGkVRspU9yHFg=='  

# Configuração da API Hugging Face
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HF_TOKEN = "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"  # Substitua pela sua chave real
db_lock = threading.Lock()
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Decorador que executa após cada requisição para configurar CORS manualmente
@app.after_request
def after_request(response):
    # Adiciona cabeçalho para permitir qualquer origem
    response.headers.add('Access-Control-Allow-Origin', '*')
    # Retorna a resposta modificada
    return response

# Define o nome do arquivo do banco de dados
DATABASE = 'Usuarios-ChefNow.sqlite'

# --- Decorador para verificar autenticação JWT ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'success': False, 'msg': 'Token não fornecido'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            current_user = {
                'id': data['user_id'],
                'email': data['email'],
                'tipo': data['tipo']  # 'cliente' ou 'chef'
            }
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'msg': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'msg': 'Token inválido'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# --- Rotas principais ---
# Rota para a página inicial
@app.route('/')
def index():
    return render_template('Index.html')

# Rota para a página de login
@app.route('/login')
def login_page():
    return render_template('login.html')

# Rota para a página de cadastro de chef
@app.route('/Cadastro-chef')
def cadastro():
    return render_template('Cadastro-chef.html')

# Rota para a página de criar conta de cliente
@app.route('/Criar-conta')
def criar_conta():
    return render_template('Criar-conta.html')

# Rota para a página de perfil do chef (protegida)
@app.route('/Perfil-chef')
def perfil_chef():
    return render_template('Perfil-chef.html')



# --- Rotas de Autenticação ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    tipo_usuario = data.get('tipo')  # 'cliente' ou 'chef'
    
    if not email or not password or not tipo_usuario:
        return jsonify({'success': False, 'msg': 'Preencha todos os campos!'}), 400
    
    if tipo_usuario not in ['cliente', 'chef']:
        return jsonify({'success': False, 'msg': 'Tipo de usuário inválido!'}), 400
    
    password_hash = hashlib.sha512(password.encode()).hexdigest()
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Determina a tabela baseada no tipo de usuário
        tabela = 'cliente' if tipo_usuario == 'cliente' else 'chefs'
        
        cursor.execute(f'''
            SELECT id, nome, email FROM {tabela}
            WHERE email = ? AND password = ?
        ''', (email, password_hash))
        
        usuario = cursor.fetchone()
        conn.close()
        
        if usuario:
            # Gera o token JWT
            payload = {
                'user_id': usuario[0],
                'email': usuario[2],
                'nome': usuario[1],
                'tipo': tipo_usuario,
                'exp': datetime.utcnow() + timedelta(hours=24)  # Token expira em 24 horas
            }
            
            token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
            
            return jsonify({
                'success': True,
                'msg': 'Login realizado com sucesso!',
                'token': token,
                'user': {
                    'id': usuario[0],
                    'nome': usuario[1],
                    'email': usuario[2],
                    'tipo': tipo_usuario
                }
            })
        else:
            return jsonify({'success': False, 'msg': 'Email ou senha incorretos!'}), 401
    
    except Exception as e:
        print(f"Erro no login: {e}")
        return jsonify({'success': False, 'msg': 'Erro interno no servidor.'}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    # Como JWT é stateless, o logout é feito no frontend removendo o token
    return jsonify({'success': True, 'msg': 'Logout realizado com sucesso!'})

@app.route('/api/verificar-token', methods=['GET'])
@token_required
def verificar_token(current_user):
    return jsonify({
        'success': True,
        'user': current_user
    })

# --- Rota do Chat Hugging Face ---
@app.route('/Chatbot', methods=['GET', 'POST'])
def Chatbot():
    resposta = None
    if request.method == 'POST':
        pergunta = request.form['pergunta']
        prompt = f"<s>[INST] {pergunta} [/INST]"

        payload = {
            "inputs": prompt,
            "options": {"wait_for_model": True}
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # A resposta vem em "generated_text" dentro de uma lista
            resposta = result[0]['generated_text'].split('[/INST]')[-1].strip()
        except Exception as e:
            resposta = f"Erro ao acessar a API: {e}"

    return render_template('Chatbot.html', resposta=resposta)

# --- Funcionalidades de busca ---
# Rota para buscar chefs próximos baseado no CEP (protegida)
@app.route('/chefs-proximos')
@token_required
def chefs_proximos(current_user):
    cep_base = request.args.get('cep')
    raio = int(request.args.get('raio', 50))  # valor padrão: 50

    if not cep_base or not cep_base.isdigit():
        return jsonify({'erro': 'CEP inválido'}), 400

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        query = """
            SELECT id, nome, email, cep,
                   ABS(CAST(cep AS INTEGER) - CAST(? AS INTEGER)) AS diferenca
            FROM chefs
            WHERE ABS(CAST(cep AS INTEGER) - CAST(? AS INTEGER)) <= ?
            ORDER BY diferenca ASC;
        """

        cursor.execute(query, (cep_base, cep_base, raio))
        resultados = cursor.fetchall()
        conn.close()

        proximos = []
        for id_, nome, email, cep, diferenca in resultados:
            print(f"Chef encontrado: {nome}, Email: {email}, CEP: {cep}")
            proximos.append({
                'id': id_,
                'nome': nome,
                'email': email,
                'cep': cep,
            })

        return jsonify(proximos)
    
    except Exception as e:
        print(f"Erro ao buscar chefs próximos: {e}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500

# --- Configurações de banco de dados ---
def Conectar_banco_dados():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    return cursor, conn

def criar_banco_dados():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cliente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            nascimento TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chefs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            nascimento TEXT NOT NULL,
            cep TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

# --- Cadastro de cliente ---
@app.route('/enviar', methods=['POST'])
def enviar():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    password = data.get('password')
    cpf = data.get('cpf')
    nascimento = data.get('nascimento')

    if not nome or not email or not password or not cpf or not nascimento:
        return jsonify({'success': False, 'msg': 'Preencha todos os campos!'}), 400

    password_hash = hashlib.sha512(password.encode()).hexdigest()

    try:
        with db_lock:
            cursor_sql, conexcao = Conectar_banco_dados()
            print("ente")
            cursor_sql.execute('''
                INSERT INTO cliente (nome, email, password, cpf, nascimento)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, email, password_hash, cpf, nascimento))
            conexcao.commit()
            conexcao.close()

        return jsonify({'success': True, 'msg': 'Cadastro realizado com sucesso!'})
    
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'msg': 'Email ou CPF já cadastrados.'}), 409
    except Exception as e:
        print(f"Erro no cadastro: {e}")
        return jsonify({'success': False, 'msg': 'Erro interno no servidor.'}), 500

# --- Cadastro de chef ---
@app.route('/cadastrar-chef', methods=['POST'])
def cadastrar_chef():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    password = data.get('password')
    cpf = data.get('cpf')
    nascimento = data.get('nascimento')
    cep = data.get('cep')

    if not all([nome, email, password, cpf, nascimento, cep]):
        return jsonify({'success': False, 'msg': 'Preencha todos os campos!'}), 400

    if not cep.isdigit():
        return jsonify({'success': False, 'msg': 'CEP deve conter apenas números!'}), 400

    password_hash = hashlib.sha512(password.encode()).hexdigest()

    try:
        with db_lock:
            cursor_sql, conexcao = Conectar_banco_dados()
            cursor_sql.execute('''
                INSERT INTO chefs (nome, email, password, cpf, nascimento, cep)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, email, password_hash, cpf, nascimento, cep))
            conexcao.commit()
            conexcao.close()

        return jsonify({'success': True, 'msg': 'Chef cadastrado com sucesso!'})
    
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'msg': 'Email ou CPF já cadastrados.'}), 409
    except Exception as e:
        print(f"Erro no cadastro do chef: {e}")
        return jsonify({'success': False, 'msg': 'Erro interno no servidor.'}), 500

# --- Inicialização da aplicação ---
if __name__ == '__main__':
    criar_banco_dados()
    app.run(debug=True)