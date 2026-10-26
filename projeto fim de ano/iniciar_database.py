from app.database import DatabaseManager
from app.models.user import UserModel

def init_db():
    print("-> Criando/Atualizando a estrutura do banco de dados...")
    
    with DatabaseManager() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        db.execute("""
        CREATE TABLE IF NOT EXISTS decks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            carta_principal TEXT,
            lista_baralho TEXT,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES usuarios (id) ON DELETE CASCADE
        );
        """)
        
    print("-> Estrutura do banco verificada com sucesso!")

    if not UserModel.get_by_username("ash"):
        UserModel.create("ash", "pikachu123")

if __name__ == '__main__':
    init_db()