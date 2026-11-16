from app.db import DatabaseConnection
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:
    def __init__(self, username, password=None, password_hash=None, id=None, created_at=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash or (generate_password_hash(password) if password else None)
        self.created_at = created_at

    def verificar_senha(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def salvar(self):
        if self.id is None:
            with DatabaseConnection() as db:
                sql = "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)"
                db.cursor.execute(sql, (self.username, self.password_hash))
                self.id = db.cursor.lastrowid
        else:
            with DatabaseConnection() as db:
                sql = "UPDATE usuarios SET username = ?, password_hash = ? WHERE id = ?"
                db.cursor.execute(sql, (self.username, self.password_hash, self.id))
        return self

    def excluir(self):
        if self.id:
            with DatabaseConnection() as db:
                sql = "DELETE FROM usuarios WHERE id = ?"
                db.cursor.execute(sql, (self.id,))
            self.id = None

    @classmethod
    def _from_row(cls, row):
        if not row:
            return None
        return cls(
            id=row['id'],
            username=row['username'],
            password_hash=row['password_hash'],
            created_at=row['created_at']
        )

    @classmethod
    def buscar_por_username(cls, username):
        with DatabaseConnection() as db:
            sql = "SELECT id, username, password_hash, created_at FROM usuarios WHERE username = ?"
            db.cursor.execute(sql, (username,))
            row = db.cursor.fetchone()
            return cls._from_row(row)

    @classmethod
    def buscar_por_id(cls, usuario_id):
        with DatabaseConnection() as db:
            sql = "SELECT id, username, password_hash, created_at FROM usuarios WHERE id = ?"
            db.cursor.execute(sql, (usuario_id,))
            row = db.cursor.fetchone()
            return cls._from_row(row)
