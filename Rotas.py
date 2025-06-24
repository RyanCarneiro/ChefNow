# ============================
# PARTE 1: IMPORTAÇÕES
# ============================

# Imports para Flask e funcionalidades básicas
import threading  # Para thread safety (múltiplos usuários simultâneos)
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import sqlite3    # Banco de dados SQLite
import os         # Operações do sistema operacional
import hashlib    # Para criptografar senhas
import jwt        # Para criar tokens de autenticação
from datetime import datetime, timedelta  # Para trabalhar com datas
from functools import wraps  # Para criar decoradores

# Imports para o chat Hugging Face
import requests   # Para fazer requisições HTTP

# ============================
# PARTE 2: CONFIGURAÇÃO INICIAL
# ============================

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Chave secreta para assinar tokens JWT (como uma "senha master")
# Esta chave é usada para garantir que os tokens não foram falsificados
JWT_SECRET = 'qTLzPaVdyNjMPM+Z3d38N9hV0a3f0WeGblcPjJTA6UOmujDsXxgFcDhF6F1k9x7A2cUzIatMQ//m8zBQ64YuvNWZQkz9k7B2vSxez8yt8DJsdUbFZzG6zU2TAarAiM/h5bcXnlmHe9VwGkVRspU9yHFg=='  

# Configuração da API Hugging Face (para o chatbot)
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HF_TOKEN = "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"  # Token da API

# Lock para evitar problemas quando múltiplas pessoas acessam o banco ao mesmo tempo
db_lock = threading.Lock()

# Cabeçalhos para requisições da API do Hugging Face
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# ============================
# PARTE 3: CONFIGURAÇÃO CORS
# ============================

# Decorador que executa após cada requisição para permitir CORS
# CORS = Cross-Origin Resource Sharing (permite que frontend acesse o backend)
@app.after_request
def after_request(response):
    # Permite que qualquer site faça requisições para esta API
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Nome do arquivo do banco de dados
DATABASE = 'Usuarios-ChefNow.sqlite'

# ============================
# PARTE 4: DECORADOR DE AUTENTICAÇÃO (MUITO IMPORTANTE!)
# ============================

# Este decorador é como um "segurança" que verifica se a pessoa está logada
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Pega o token do cabeçalho Authorization da requisição
        token = request.headers.get('Authorization')
        
        # Se não tem token, pessoa não está logada
        if not token:
            return jsonify({'success': False, 'msg': 'Token não fornecido'}), 401
        
        try:
            # Remove a palavra "Bearer " do início do token
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            
            # Decodifica o token usando a chave secreta
            # É como "abrir" o token para ver as informações dentro
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            
            # Extrai as informações do usuário do token
            current_user = {
                'id': data['user_id'],
                'email': data['email'],
                'tipo': data['tipo']  # 'cliente' ou 'chef'
            }
            
        except jwt.ExpiredSignatureError:
            # Token expirado (passou de 24 horas)
            return jsonify({'success': False, 'msg': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            # Token inválido (foi alterado ou corrompido)
            return jsonify({'success': False, 'msg': 'Token inválido'}), 401
        
        # Se chegou até aqui, o token é válido!
        # Chama a função original passando as informações do usuário
        return f(current_user, *args, **kwargs)
    
    return decorated

# ============================
# PARTE 5: ROTAS DAS PÁGINAS HTML
# ============================

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('Index.html')

# Rota para a página de login
@app.route('/login')
def login_page():
    return render_template('login-chefnow.html')

# Rota para a página de cadastro de chef
@app.route('/Cadastro-chef')
def cadastro():
    return render_template('Cadastro-chef.html')

# Rota para a página de criar conta de cliente
@app.route('/Criar-conta')
def criar_conta():
    return render_template('Criar-conta.html')

# Rota para a página de perfil do chef (protegida pelo token)
@app.route('/Perfil-chef')
def perfil_chef():
    return render_template('Perfil-chef.html')

# ============================
# PARTE 6: ROTA DE LOGIN (CORE DO SISTEMA!)
# ============================

@app.route('/api/login', methods=['POST'])
def login():
    # Pega os dados enviados pelo frontend (JavaScript)
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    tipo_usuario = data.get('tipo')  # 'cliente' ou 'chef'
    
    # VALIDAÇÃO 1: Verifica se todos os campos foram preenchidos
    if not email or not password or not tipo_usuario:
        return jsonify({'success': False, 'msg': 'Preencha todos os campos!'}), 400
    
    # VALIDAÇÃO 2: Verifica se o tipo de usuário é válido
    if tipo_usuario not in ['cliente', 'chef']:
        return jsonify({'success': False, 'msg': 'Tipo de usuário inválido!'}), 400
    
    # SEGURANÇA: Criptografa a senha usando SHA-512
    # Nunca armazenamos senhas em texto plano no banco!
    password_hash = hashlib.sha512(password.encode()).hexdigest()
    
    try:
        # CONEXÃO COM BANCO DE DADOS
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # ESCOLHE A TABELA: cliente ou chefs
        tabela = 'cliente' if tipo_usuario == 'cliente' else 'chefs'
        
        # BUSCA O USUÁRIO: procura por email e senha criptografada
        cursor.execute(f'''
            SELECT id, nome, email FROM {tabela}
            WHERE email = ? AND password = ?
        ''', (email, password_hash))
        
        # Pega o resultado da busca
        usuario = cursor.fetchone()
        conn.close()
        
        # VERIFICAÇÃO: Se encontrou o usuário...
        if usuario:
            # CRIAÇÃO DO TOKEN JWT
            # O token é como um "cartão de identificação digital"
            payload = {
                'user_id': usuario[0],    # ID do usuário
                'email': usuario[2],      # Email do usuário
                'nome': usuario[1],       # Nome do usuário
                'tipo': tipo_usuario,     # Tipo (cliente/chef)
                'exp': datetime.utcnow() + timedelta(hours=24)  # Expira em 24 horas
            }
            
            # "Assina" o token com a chave secreta (como um carimbo oficial)
            token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
            
            # SUCESSO: Retorna o token e informações do usuário
            return jsonify({
                'success': True,
                'msg': 'Login realizado com sucesso!',
                'token': token,  # Este token vai para o localStorage no frontend
                'user': {
                    'id': usuario[0],
                    'nome': usuario[1],
                    'email': usuario[2],
                    'tipo': tipo_usuario
                }
            })
        else:
            # FALHA: Usuário não encontrado ou senha errada
            return jsonify({'success': False, 'msg': 'Email ou senha incorretos!'}), 401
    
    except Exception as e:
        # ERRO: Algo deu errado (banco fora do ar, etc.)
        print(f"Erro no login: {e}")
        return jsonify({'success': False, 'msg': 'Erro interno no servidor.'}), 500

# ============================
# PARTE 7: OUTRAS ROTAS DE AUTENTICAÇÃO
# ============================

# Rota de logout (simples, pois JWT é stateless)
@app.route('/api/logout', methods=['POST'])
def logout():
    # Com JWT, o logout é feito no frontend removendo o token
    # Aqui só confirmamos que o logout foi "processado"
    return jsonify({'success': True, 'msg': 'Logout realizado com sucesso!'})

# Rota para verificar se o token ainda é válido
@app.route('/api/verificar-token', methods=['GET'])
@token_required  # Usa o decorador de segurança
def verificar_token(current_user):
    # Se chegou até aqui, o token é válido (decorador já verificou)
    return jsonify({
        'success': True,
        'user': current_user
    })

# ============================
# PARTE 8: ROTA DO CHATBOT
# ============================

@app.route('/Chatbot', methods=['GET', 'POST'])
def Chatbot():
    resposta = None
    if request.method == 'POST':
        # Pega a pergunta do usuário
        pergunta = request.form['pergunta']
        # Formata a pergunta para o modelo de IA
        prompt = f"<s>[INST] {pergunta} [/INST]"

        # Prepara os dados para enviar para a API
        payload = {
            "inputs": prompt,
            "options": {"wait_for_model": True}
        }

        try:
            # Faz a requisição para a API do Hugging Face
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # Extrai a resposta do modelo
            resposta = result[0]['generated_text'].split('[/INST]')[-1].strip()
        except Exception as e:
            resposta = f"Erro ao acessar a API: {e}"

    return render_template('Chatbot.html', resposta=resposta)

# ============================
# PARTE 9: BUSCA DE CHEFS PRÓXIMOS
# ============================

@app.route('/chefs-proximos')
@token_required  # Só usuários logados podem buscar chefs
def chefs_proximos(current_user):
    # Pega o CEP base e raio de busca dos parâmetros da URL
    cep_base = request.args.get('cep')
    raio = int(request.args.get('raio', 50))  # padrão: 50km

    # Validação do CEP
    if not cep_base or not cep_base.isdigit():
        return jsonify({'erro': 'CEP inválido'}), 400

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Query para buscar chefs próximos baseado na diferença de CEP
        # (Esta é uma aproximação simples, não é geograficamente precisa)
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

        # Formata os resultados
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

# ============================
# PARTE 10: FUNÇÕES DO BANCO DE DADOS
# ============================

def Conectar_banco_dados():
    """Conecta ao banco de dados e retorna cursor e conexão"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    return cursor, conn

def criar_banco_dados():
    """Cria as tabelas do banco de dados se não existirem"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabela de clientes
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
    
    # Tabela de chefs
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

# ============================
# PARTE 11: CADASTRO DE CLIENTE
# ============================

@app.route('/enviar', methods=['POST'])
def enviar():
    # Pega os dados do formulário
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    password = data.get('password')
    cpf = data.get('cpf')
    nascimento = data.get('nascimento')

    # Validação dos campos
    if not nome or not email or not password or not cpf or not nascimento:
        return jsonify({'success': False, 'msg': 'Preencha todos os campos!'}), 400

    # Criptografa a senha
    password_hash = hashlib.sha512(password.encode()).hexdigest()

    try:
        # Usa lock para evitar problemas de concorrência
        with db_lock:
            cursor_sql, conexcao = Conectar_banco_dados()
            print("Cadastrando cliente...")
            
            # Insere o cliente no banco
            cursor_sql.execute('''
                INSERT INTO cliente (nome, email, password, cpf, nascimento)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, email, password_hash, cpf, nascimento))
            
            conexcao.commit()
            conexcao.close()

        return jsonify({'success': True, 'msg': 'Cadastro realizado com sucesso!'})
    
    except sqlite3.IntegrityError:
        # Email ou CPF já existem no banco
        return jsonify({'success': False, 'msg': 'Email ou CPF já cadastrados.'}), 409
    except Exception as e:
        print(f"Erro no cadastro: {e}")
        return jsonify({'success': False, 'msg': 'Erro interno no servidor.'}), 500

# ============================
# PARTE 12: CADASTRO DE CHEF
# ============================

@app.route('/cadastrar-chef', methods=['POST'])
def cadastrar_chef():
    # Pega os dados do formulário
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    password = data.get('password')
    cpf = data.get('cpf')
    nascimento = data.get('nascimento')
    cep = data.get('cep')

    # Validação: todos os campos obrigatórios
    if not all([nome, email, password, cpf, nascimento, cep]):
        return jsonify({'success': False, 'msg': 'Preencha todos os campos!'}), 400

    # Validação: CEP deve ser só números
    if not cep.isdigit():
        return jsonify({'success': False, 'msg': 'CEP deve conter apenas números!'}), 400

    # Criptografa a senha
    password_hash = hashlib.sha512(password.encode()).hexdigest()

    try:
        # Usa lock para evitar problemas de concorrência
        with db_lock:
            cursor_sql, conexcao = Conectar_banco_dados()
            
            # Insere o chef no banco
            cursor_sql.execute('''
                INSERT INTO chefs (nome, email, password, cpf, nascimento, cep)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, email, password_hash, cpf, nascimento, cep))
            
            conexcao.commit()
            conexcao.close()

        return jsonify({'success': True, 'msg': 'Chef cadastrado com sucesso!'})
    
    except sqlite3.IntegrityError:
        # Email ou CPF já existem
        return jsonify({'success': False, 'msg': 'Email ou CPF já cadastrados.'}), 409
    except Exception as e:
        print(f"Erro no cadastro do chef: {e}")
        return jsonify({'success': False, 'msg': 'Erro interno no servidor.'}), 500

# ============================
# PARTE 13: INICIALIZAÇÃO DA APLICAÇÃO
# ============================

if __name__ == '__main__':
    # Cria o banco de dados se não existir
    criar_banco_dados()
    # Inicia o servidor Flask em modo debug
    app.run(debug=True)