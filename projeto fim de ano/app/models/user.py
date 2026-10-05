from app.database import DatabaseManager
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    def __init__(self, username, password=None, password_hash=None, id=None, created_at=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash or (generate_password_hash(password) if password else None)
        self.created_at = created_at

    # ============================================================
    # MÉTODOS DE COMPORTAMENTO DA INSTÂNCIA (ACTIVE RECORD)
    # ============================================================

    def check_password(self, password):
        """Valida a senha fornecida comparando com o Hash do objeto."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def save(self):
        """[ACTIVE RECORD] Salva o objeto no banco de dados.
        Realiza INSERT se for novo ou UPDATE se já possuir ID."""
        if self.id is None:
            # Inserção de novo registro
            with DatabaseManager() as db:
                query = "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)"
                db.execute(query, (self.username, self.password_hash))
                self.id = db.cursor.lastrowid
        else:
            # Atualização de registro existente
            with DatabaseManager() as db:
                query = "UPDATE usuarios SET username = ?, password_hash = ? WHERE id = ?"
                db.execute(query, (self.username, self.password_hash, self.id))
        return self

    def update_password(self, new_password):
        """[ACTIVE RECORD] Altera a senha da instância e persiste no banco."""
        self.password_hash = generate_password_hash(new_password)
        return self.save()

    def delete(self):
        """[ACTIVE RECORD] Remove o próprio registro do banco de dados."""
        if self.id:
            with DatabaseManager() as db:
                query = "DELETE FROM usuarios WHERE id = ?"
                db.execute(query, (self.id,))
            self.id = None

    # ============================================================
    # MÉTODOS DE CLASSE / CONSULTAS (ACTIVE RECORD FINDERS)
    # ============================================================

    @classmethod
    def _from_row(cls, row):
        """Converte um resultado sqlite3.Row em uma instância de UserModel."""
        if not row:
            return None
        return cls(
            id=row['id'],                 # Acesso pelo nome da coluna via sqlite3.Row
            username=row['username'],     # Acesso pelo nome da coluna via sqlite3.Row
            password_hash=row['password_hash'],
            created_at=row['created_at']
        )

    @classmethod
    def create(cls, username, password):
        """[FINDER / CREATOR] Cria e persiste diretamente um novo usuário."""
        user = cls(username=username, password=password)
        return user.save()

    @classmethod
    def get_by_username(cls, username):
        """[FINDER] Busca um usuário pelo nome de usuário."""
        with DatabaseManager() as db:
            query = "SELECT id, username, password_hash, created_at FROM usuarios WHERE username = ?"
            db.execute(query, (username,))
            row = db.fetchone()
            return cls._from_row(row)

    @classmethod
    def get_by_id(cls, user_id):
        """[FINDER] Busca um usuário pelo ID primário."""
        with DatabaseManager() as db:
            query = "SELECT id, username, password_hash, created_at FROM usuarios WHERE id = ?"
            db.execute(query, (user_id,))
            row = db.fetchone()
            return cls._from_row(row)

    @classmethod
    def all(cls):
        """[FINDER] Retorna uma lista com todos os usuários cadastrados."""
        with DatabaseManager() as db:
            query = "SELECT id, username, password_hash, created_at FROM usuarios"
            db.execute(query)
            rows = db.fetchall()
            return [cls._from_row(row) for row in rows]