# Importa a classe Flask para criar a aplicação web
from flask import Flask, request, jsonify, render_template
# Importa sqlite3 para trabalhar com banco de dados SQLite
import sqlite3
# Importa os para trabalhar com sistema operacional
import os
# Importa hashlib para criptografar senhas
import hashlib

# Cria uma instância da aplicação Flask
app = Flask(__name__)

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
    # Renderiza o template da página inicial
    return render_template('Index.html')

# Rota para a página de cadastro de chef
@app.route('/Cadastro-chef')
def cadastro():
    # Renderiza o template da página de cadastro de chef
    return render_template('Cadastro-chef.html')

# Rota para a página de criar conta de cliente
@app.route('/Criar-conta')
def criar_conta():
    # Renderiza o template da página de criar conta
    return render_template('Criar-conta.html')

# Rota para a página de perfil do chef
@app.route('/Perfil-chef')
def perfil_chef():
    # Renderiza o template passando os dados do chef
    return render_template('Perfil-chef.html')

# Rota para buscar chefs próximos baseado no CEP
@app.route('/chefs-proximos')
def chefs_proximos():
    # Obtém o CEP base dos parâmetros da URL
    cep_base = request.args.get('cep')
    # Obtém o raio de busca (padrão: 50) e converte para inteiro
    raio = int(request.args.get('raio', 50))  # valor padrão: 50

    # Valida se o CEP foi fornecido e se contém apenas números
    if not cep_base or not cep_base.isdigit():
        # Retorna erro 400 se CEP for inválido
        return jsonify({'erro': 'CEP inválido'}), 400

    # Bloco try-except para capturar erros
    try:
        # Conecta ao banco de dados
        conn = sqlite3.connect(DATABASE)
        # Cria cursor para executar comandos SQL
        cursor = conn.cursor()

        # Query SQL para buscar chefs próximos baseado na diferença de CEP
        query = """
            SELECT id, nome, email, cep,
                   ABS(CAST(cep AS INTEGER) - CAST(? AS INTEGER)) AS diferenca
            FROM chefs
            WHERE ABS(CAST(cep AS INTEGER) - CAST(? AS INTEGER)) <= ?
            ORDER BY diferenca ASC;
        """

        # Executa a query com os parâmetros (cep_base, cep_base, raio)
        cursor.execute(query, (cep_base, cep_base, raio))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Fecha a conexão com o banco
        conn.close()

        # Lista para armazenar os chefs próximos
        proximos = []
        # Itera sobre cada resultado da consulta
        for id_, nome, email, cep, diferenca in resultados:
            # Imprime informações do chef encontrado (para debug)
            print(f"Chef encontrado: {nome}, Email: {email}, CEP: {cep}")
            # Adiciona o chef à lista de próximos
            proximos.append({
                'id': id_,
                'nome': nome,
                'email': email,
                'cep': cep,
            })

        # Retorna a lista de chefs próximos em formato JSON
        return jsonify(proximos)
    
    # Captura qualquer exceção que possa ocorrer
    except Exception as e:
        # Imprime o erro no console (para debug)
        print(f"Erro ao buscar chefs próximos: {e}")
        # Retorna erro 500 (erro interno do servidor)
        return jsonify({'erro': 'Erro interno no servidor'}), 500

# --- Configurações de banco de dados ---
# Função para conectar ao banco de dados
def Conectar_banco_dados():
    # Conecta ao banco SQLite
    conn = sqlite3.connect(DATABASE)
    # Cria cursor para executar comandos
    cursor = conn.cursor()
    # Retorna cursor e conexão
    return cursor, conn

# Função para criar as tabelas do banco de dados
def criar_banco_dados():
    # Conecta ao banco de dados
    conn = sqlite3.connect(DATABASE)
    # Cria cursor
    cursor = conn.cursor()
    # Executa SQL para criar tabela de clientes se não existir
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
    # Executa SQL para criar tabela de chefs se não existir
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
    # Confirma as alterações no banco
    conn.commit()
    # Fecha a conexão
    conn.close()

# --- Cadastro de cliente ---
# Rota para cadastrar cliente (aceita apenas POST)
@app.route('/enviar', methods=['POST'])
def enviar():
    # Obtém dados JSON da requisição
    data = request.get_json()
    # Extrai cada campo dos dados recebidos
    nome = data.get('nome')
    email = data.get('email')
    password = data.get('password')
    cpf = data.get('cpf')
    nascimento = data.get('nascimento')

    # Valida se todos os campos foram preenchidos
    if not nome or not email or not password or not cpf or not nascimento:
        # Retorna erro 400 se algum campo estiver vazio
        return jsonify({'success': False, 'msg': 'Preencha todos os campos!'}), 400

    # Hash da senha para segurança usando SHA-512
    password_hash = hashlib.sha512(password.encode()).hexdigest()

    # Bloco try-except para capturar erros
    try:
        # Conecta ao banco de dados
        cursor_sql, conexcao = Conectar_banco_dados()
        # Executa SQL para inserir novo cliente
        cursor_sql.execute('''
            INSERT INTO cliente (nome, email, password, cpf, nascimento)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, email, password_hash, cpf, nascimento))
        # Confirma a inserção
        conexcao.commit()
        # Fecha a conexão
        conexcao.close()

        # Retorna sucesso se cadastro foi realizado
        return jsonify({'success': True, 'msg': 'Cadastro realizado com sucesso!'})
    
    # Captura erro de integridade (email ou CPF duplicados)
    except sqlite3.IntegrityError:
        # Retorna erro 409 (conflito) para dados duplicados
        return jsonify({'success': False, 'msg': 'Email ou CPF já cadastrados.'}), 409
    # Captura qualquer outra exceção
    except Exception as e:
        # Imprime erro no console (para debug)
        print(f"Erro no cadastro: {e}")
        # Retorna erro 500 (erro interno do servidor)
        return jsonify({'success': False, 'msg': 'Erro interno no servidor.'}), 500

# --- Cadastro de chef ---
# Rota para cadastrar chef (aceita apenas POST)
@app.route('/cadastrar-chef', methods=['POST'])
def cadastrar_chef():
    # Obtém dados JSON da requisição
    data = request.get_json()
    # Extrai cada campo dos dados recebidos
    nome = data.get('nome')
    email = data.get('email')
    password = data.get('password')
    cpf = data.get('cpf')
    nascimento = data.get('nascimento')
    cep = data.get('cep')

    # Valida se todos os campos foram preenchidos usando all()
    if not all([nome, email, password, cpf, nascimento, cep]):
        # Retorna erro 400 se algum campo estiver vazio
        return jsonify({'success': False, 'msg': 'Preencha todos os campos!'}), 400

    # Valida se CEP contém apenas números
    if not cep.isdigit():
        # Retorna erro 400 se CEP for inválido
        return jsonify({'success': False, 'msg': 'CEP deve conter apenas números!'}), 400

    # Hash da senha para segurança usando SHA-512
    password_hash = hashlib.sha512(password.encode()).hexdigest()

    # Bloco try-except para capturar erros
    try:
        # Conecta ao banco de dados
        cursor_sql, conexcao = Conectar_banco_dados()
        # Executa SQL para inserir novo chef
        cursor_sql.execute('''
            INSERT INTO chefs (nome, email, password, cpf, nascimento, cep)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, email, password_hash, cpf, nascimento, cep))
        # Confirma a inserção
        conexcao.commit()
        # Fecha a conexão
        conexcao.close()

        # Retorna sucesso se cadastro foi realizado
        return jsonify({'success': True, 'msg': 'Chef cadastrado com sucesso!'})
    
    # Captura erro de integridade (email ou CPF duplicados)
    except sqlite3.IntegrityError:
        # Retorna erro 409 (conflito) para dados duplicados
        return jsonify({'success': False, 'msg': 'Email ou CPF já cadastrados.'}), 409
    # Captura qualquer outra exceção
    except Exception as e:
        # Imprime erro no console (para debug)
        print(f"Erro no cadastro do chef: {e}")
        # Retorna erro 500 (erro interno do servidor)
        return jsonify({'success': False, 'msg': 'Erro interno no servidor.'}), 500

# --- Inicialização da aplicação ---
# Verifica se o arquivo está sendo executado diretamente
if __name__ == '__main__':
    # Criar banco de dados na inicialização da aplicação
    criar_banco_dados()
    # Inicia o servidor Flask em modo debug
    app.run(debug=True)