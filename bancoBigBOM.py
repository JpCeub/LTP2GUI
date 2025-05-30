import sqlite3
from sqlite3 import IntegrityError

DB_NAME = "Big_Bom.db"

def iniciar_conexao():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prateleiras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        id_prateleira INTEGER,
        FOREIGN KEY (id_prateleira) REFERENCES prateleiras(id) ON DELETE CASCADE
    )""")
    conn.commit()
    conn.close()

def inserir_prateleira(nome):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prateleiras (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def listar_prateleiras():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM prateleiras")
    dados = cursor.fetchall()
    conn.close()
    return dados

def deletar_prateleira(prateleira_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM produtos WHERE id_prateleira = ?", (prateleira_id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise IntegrityError("Existem produtos vinculados a esta prateleira.")
    cursor.execute("DELETE FROM prateleiras WHERE id = ?", (prateleira_id,))
    conn.commit()
    conn.close()

def atualizar_prateleira(prateleira_id, novo_nome):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE prateleiras SET nome = ? WHERE id = ?", (novo_nome, prateleira_id))
    conn.commit()
    conn.close()

def inserir_produto(nome, preco, prateleira_nome):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM prateleiras WHERE nome = ?", (prateleira_nome,))
    resultado = cursor.fetchone()
    if resultado:
        id_prateleira = resultado[0]
        cursor.execute("INSERT INTO produtos (nome, preco, id_prateleira) VALUES (?, ?, ?)",
                       (nome, preco, id_prateleira))
        conn.commit()
    conn.close()

def listar_produtos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT produtos.id, produtos.nome, produtos.preco, prateleiras.nome
        FROM produtos
        JOIN prateleiras ON produtos.id_prateleira = prateleiras.id
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados

def deletar_produto(produto_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()

def atualizar_produto(produto_id, novo_nome, novo_preco, nova_prateleira_nome):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM prateleiras WHERE nome = ?", (nova_prateleira_nome,))
    resultado = cursor.fetchone()
    if not resultado:
        conn.close()
        raise ValueError("Prateleira não encontrada.")
    id_prateleira = resultado[0]
    cursor.execute(
        "UPDATE produtos SET nome = ?, preco = ?, id_prateleira = ? WHERE id = ?",
        (novo_nome, novo_preco, id_prateleira, produto_id)
    )
    conn.commit()
    conn.close()


