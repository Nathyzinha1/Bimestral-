# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('ze_pinheiros.db')
    cursor = conn.cursor()

    # Criação das tabelas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fornecedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        contato TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        categoria_id INTEGER,
        fornecedor_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES categorias (id),
        FOREIGN KEY (fornecedor_id) REFERENCES fornecedores (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_pedido TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedido_produto (
        pedido_id INTEGER,
        produto_id INTEGER,
        PRIMARY KEY (pedido_id, produto_id),
        FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
        FOREIGN KEY (produto_id) REFERENCES produtos (id)
    )
    ''')

    conn.commit()
    conn.close()

# Executa a função para inicializar o banco de dados
if __name__ == '__main__':
    init_db()
