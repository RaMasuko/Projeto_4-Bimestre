from app.database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    def __init__(self, id, username, password_hash, created_at=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create(cls, username, password):
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)"
        cursor.execute(query, (username, hashed_password))
        conn.commit()
        
        cursor.close()
        conn.close()

    @classmethod
    def get_by_username(cls, username):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT id, username, password_hash, created_at FROM usuarios WHERE username = ?"
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if row:
            return cls(id=row['id'], username=row['username'], password_hash=row['password_hash'], created_at=row['created_at'])
        return None

    def update_password(self, new_password):
        new_hash = generate_password_hash(new_password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "UPDATE usuarios SET password_hash = ? WHERE id = ?"
        cursor.execute(query, (new_hash, self.id))
        conn.commit()
        
        cursor.close()
        conn.close()

    def delete(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM usuarios WHERE id = ?"
        cursor.execute(query, (self.id,))
        conn.commit()
        
        cursor.close()
        conn.close()