import sqlite3
import os

# Caminho do arquivo do banco de dados na pasta do projeto
DB_PATH = os.path.join(os.path.dirname(__file__), 'pokemon_deck.db')

def get_db_connection():
    """Conecta ao arquivo SQLite local sem precisar de drivers instalados."""
    conn = sqlite3.connect(DB_PATH)
    # Permite acessar colunas pelo nome (ex: row['username']) além de índice
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Cria a tabela de usuários em SQL puro."""
    conn = get_db_connection()
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    cursor.execute(create_table_sql)
    conn.commit()
    cursor.close()
    conn.close()