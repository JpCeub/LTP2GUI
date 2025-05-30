import sqlite3
from sqlite3 import IntegrityError

conn = sqlite3.connect("estoque.db")
cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS prateleiras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    ''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            id_prateleira INTEGER,
            FOREIGN KEY (id_prateleira) REFERENCES prateleiras(id) ON DELETE SET NULL
        )
    ''')

conn.commit()
    

# CRUD para Prateleiras
def inserir_prateleira(nome):
    try:
        cursor.execute("INSERT INTO prateleiras (nome) VALUES (?)", (nome,))
        conn.commit()
    except IntegrityError:
        raise IntegrityError("Prateleira já existe.")
    finally:
        conn.close()

def listar_prateleiras():
    cursor.execute("SELECT * FROM prateleiras")
    return cursor.fetchall()

def deletar_prateleira(prateleira_id):
    cursor.execute("SELECT COUNT(*) FROM produtos WHERE id_prateleira = ?", (prateleira_id,))
    if cursor.fetchone()[0] > 0:
        raise IntegrityError("Existem produtos vinculados a esta prateleira.")
    cursor.execute("DELETE FROM prateleiras WHERE id = ?", (prateleira_id,))
    conn.commit()

def atualizar_prateleira(prateleira_id, novo_nome):
    cursor.execute("UPDATE prateleiras SET nome = ? WHERE id = ?", (novo_nome, prateleira_id))
    conn.commit()

# CRUD para Produtos
def inserir_produto(nome, preco, nome_prateleira):
    cursor.execute("SELECT id FROM prateleiras WHERE nome=?", (nome_prateleira,))
    prateleira = cursor.fetchone()
    if not prateleira:
        raise ValueError("Prateleira não encontrada.")
    cursor.execute("INSERT INTO produtos (nome, preco, id_prateleira) VALUES (?, ?, ?)",
                   (nome, preco, prateleira[0]))
    conn.commit()

def listar_produtos():
    cursor.execute('''
        SELECT *
        FROM produtos LEFT JOIN prateleiras ON produtos.id_prateleira = prateleiras.id
    ''')
    return cursor.fetchall()

def atualizar_produto(produto_id, novo_nome, novo_preco, nova_prateleira_nome):
    cursor.execute("SELECT id FROM prateleiras WHERE nome = ?", (nova_prateleira_nome,))
    resultado = cursor.fetchone()
    if not resultado:
        raise ValueError("Prateleira não encontrada.")
    id_prateleira = resultado[0]
    cursor.execute(
        "UPDATE produtos SET nome = ?, preco = ?, id_prateleira = ? WHERE id = ?",
        (novo_nome, novo_preco, id_prateleira, produto_id)
    )
    conn.commit()

def deletar_produto(produto_id):
    cursor.execute("DELETE FROM produtos WHERE id=?", (produto_id,))
    conn.commit()
    return cursor.rowcount

def fechar_conexao():
    conn.close()
