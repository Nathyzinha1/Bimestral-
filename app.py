# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'ze_pinheiros.db'

def db_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# CRUD para Categorias
@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        cursor.execute('INSERT INTO categorias (nome) VALUES (?)', (nome,))
        conn.commit()

    cursor.execute('SELECT * FROM categorias')
    categorias = cursor.fetchall()
    conn.close()
    return render_template('categorias.html', categorias=categorias)

@app.route('/categorias/delete/<int:id>')
def delete_categoria(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categorias WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('categorias'))

# CRUD para Fornecedores
@app.route('/fornecedores', methods=['GET', 'POST'])
def fornecedores():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        contato = request.form['contato']
        cursor.execute('INSERT INTO fornecedores (nome, contato) VALUES (?, ?)', (nome, contato))
        conn.commit()

    cursor.execute('SELECT * FROM fornecedores')
    fornecedores = cursor.fetchall()
    conn.close()
    return render_template('fornecedores.html', fornecedores=fornecedores)

@app.route('/fornecedores/delete/<int:id>')
def delete_fornecedor(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM fornecedores WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('fornecedores'))

# CRUD para Produtos
@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        categoria_id = request.form['categoria_id']
        fornecedor_id = request.form['fornecedor_id']
        cursor.execute('INSERT INTO produtos (nome, preco, categoria_id, fornecedor_id) VALUES (?, ?, ?, ?)', 
                       (nome, preco, categoria_id, fornecedor_id))
        conn.commit()

    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    cursor.execute('SELECT * FROM categorias')
    categorias = cursor.fetchall()
    cursor.execute('SELECT * FROM fornecedores')
    fornecedores = cursor.fetchall()
    conn.close()
    return render_template('produtos.html', produtos=produtos, categorias=categorias, fornecedores=fornecedores)

@app.route('/produtos/delete/<int:id>')
def delete_produto(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('produtos'))

# CRUD para Pedidos
@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        data_pedido = request.form['data_pedido']
        produto_ids = request.form.getlist('produto_ids')
        cursor.execute('INSERT INTO pedidos (data_pedido) VALUES (?)', (data_pedido,))
        pedido_id = cursor.lastrowid
        
        for produto_id in produto_ids:
            cursor.execute('INSERT INTO pedido_produto (pedido_id, produto_id) VALUES (?, ?)', (pedido_id, produto_id))
        
        conn.commit()

    cursor.execute('SELECT * FROM pedidos')
    pedidos = cursor.fetchall()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    return render_template('pedidos.html', pedidos=pedidos, produtos=produtos)

@app.route('/pedidos/delete/<int:id>')
def delete_pedido(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pedidos WHERE id = ?', (id,))
    cursor.execute('DELETE FROM pedido_produto WHERE pedido_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('pedidos'))

if __name__ == '__main__':
    app.run(debug=True)
