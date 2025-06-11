# Imports para Flask e funcionalidades básicas
from flask import Flask, request, jsonify, render_template
import sqlite3
import os
import hashlib

# Imports para o chat Hugging Face
import requests

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Configuração da API Hugging Face
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HF_TOKEN = "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"  # Substitua pela sua chave real

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

# --- Rotas principais ---
# Rota para a página inicial
@app.route('/')
def index():
    return render_template('Index.html')

# Rota para a página de cadastro de chef
@app.route('/Cadastro-chef')
def cadastro():
    return render_template('Cadastro-chef.html')

# Rota para a página de criar conta de cliente
@app.route('/Criar-conta')
def criar_conta():
    return render_template('Criar-conta.html')

# Rota para a página de perfil do chef
@app.route('/Perfil-chef')
def perfil_chef():
    return render_template('Perfil-chef.html')

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
# Rota para buscar chefs próximos baseado no CEP
@app.route('/chefs-proximos')
def chefs_proximos():
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
        cursor_sql, conexcao = Conectar_banco_dados()
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