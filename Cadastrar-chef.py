from flask import Flask, request, jsonify, render_template
import sqlite3
import os
import threading

app = Flask(__name__)
db_bloqueada = threading.Lock()
DATABASE = 'Cliente_conta.sqlite'

def Conectar_banco_dados():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    return cursor,conn

def criar_banco_dados():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chefs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            nascimento TEXT NOT NULL
            cep TEXT NOT NULL
        );
    ''')
    # conn.commit()
    # conn.close()

@app.route('/')
def index():
    return render_template('Criar-conta.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    
    cursor_sql, conexcao = Conectar_banco_dados()
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    password = data.get('password')
    cpf = data.get('cpf')
    nascimento = data.get('nascimento')

    if not nome or not email or not password or not cpf or not nascimento:
        return jsonify({'success': False, 'msg': 'Preencha todos os campos!'}), 400

    try:
        with db_bloqueada:
            cursor_sql.execute('''
                INSERT INTO cliente (nome, email, password, cpf, nascimento)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, email, password, cpf, nascimento))
            conexcao.commit()

            conexcao.close()

        return jsonify({'success': True, 'msg': 'Cadastro realizado com sucesso!'})
    except sqlite3.IntegrityError as e:
        return jsonify({'success': False, 'msg': 'Email ou CPF já cadastrados.'}), 409
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'msg': 'Erro interno no servidor.' + e}), 500

if __name__ == '__main__':
    app.run(debug=True)
