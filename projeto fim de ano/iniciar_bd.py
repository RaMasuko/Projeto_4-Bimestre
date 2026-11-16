from app.db import DatabaseConnection
from app.models.user import Usuario
from app.models.deck import Deck
from app.models.carta_preco import CartaPreco

def iniciar_banco():
    print("-> Criando/Atualizando a estrutura do banco de dados...")

    with DatabaseConnection() as db:
        db.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        db.cursor.execute("""
        CREATE TABLE IF NOT EXISTS decks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            carta_principal TEXT,
            lista_baralho TEXT,
            usuario_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
        );
        """)

        db.cursor.execute("""
        CREATE TABLE IF NOT EXISTS cartas_precos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_carta TEXT NOT NULL,
            colecao TEXT NOT NULL,
            raridade TEXT NOT NULL,
            preco_estimado REAL NOT NULL,
            usuario_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
        );
        """)

    print("-> Tabelas verificadas com sucesso!")

    usuario_teste = Usuario.buscar_por_username("ash")
    if not usuario_teste:
        usuario_teste = Usuario(username="ash", password="pikachu123")
        usuario_teste.salvar()
        print("-> Usuário de teste criado: ash / pikachu123")

        deck_inicial = Deck(
            name="Charizard ex Meta",
            carta_principal="Charizard ex",
            lista_baralho="3 Charizard ex\n4 Charmander\n2 Pidgeot ex\n4 Ultra Bola\n12 Energia de Fogo",
            usuario_id=usuario_teste.id
        )
        deck_inicial.salvar()

        carta_inicial = CartaPreco(
            nome_carta="Charizard ex (SIR)",
            colecao="Obsidian Flames",
            raridade="Special Illustration Rare",
            preco_estimado=289.90,
            usuario_id=usuario_teste.id
        )
        carta_inicial.salvar()
        print("-> Registros de exemplo criados para o usuário 'ash'!")

if __name__ == '__main__':
    iniciar_banco()
