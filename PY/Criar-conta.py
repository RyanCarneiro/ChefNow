from flask import Flask, request, jsonify, render_templete
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

DATABASE = 'Cliente_conta.sqlite'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE cliente (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            senha VARCHAR(255) NOT NULL,
            cpf CHAR(11) NOT NULL UNIQUE,
            nascimento DATE NOT NULL,
            tipo BOOLEAN NOT NULL -- TRUE = chef, FALSE = cliente
        );
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_templete('Criae-conta.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nome = request.form.get('nome')
    email= request.form.get('email')
    password = request.form.get('password')
    cpf = request.form.get('cpf')
    nascimento = request.form.get('nascimento')

