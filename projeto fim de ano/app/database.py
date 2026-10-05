import sqlite3
import os

# Caminho do banco SQLite na pasta do projeto
DB_PATH = os.path.join(os.path.dirname(__file__), 'pokemon_deck.db')

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        # Permite acessar colunas pelo nome (ex: row['username'])
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()