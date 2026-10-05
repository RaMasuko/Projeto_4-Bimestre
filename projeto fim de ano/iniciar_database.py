from app.database import DatabaseManager
from app.models.user import UserModel

def init_db():
    print("-> Criando a estrutura do banco de dados...")
    
    with DatabaseManager() as db:
        # Tabela de Usuários
        db.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Tabela de Decks associada ao Usuário
        db.execute("""
        CREATE TABLE IF NOT EXISTS decks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            carta_principal TEXT,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES usuarios (id) ON DELETE CASCADE
        );
        """)
        
    print("-> Tabelas 'usuarios' e 'decks' verificadas/criadas com sucesso!")

    if not UserModel.get_by_username("ash"):
        UserModel.create("ash", "pikachu123")
        print("-> Usuário padrão 'ash' cadastrado!")

if __name__ == '__main__':
    init_db()