from app.database import DatabaseManager

class DeckModel:
    def __init__(self, name, carta_principal=None, lista_baralho=None, user_id=None, id=None):
        self.id = id
        self.name = name
        self.carta_principal = carta_principal
        self.lista_baralho = lista_baralho
        self.user_id = user_id

    @classmethod
    def _from_row(cls, row):
        if not row:
            return None
        return cls(
            id=row['id'],
            name=row['name'],
            carta_principal=row['carta_principal'],
            lista_baralho=row['lista_baralho'],
            user_id=row['user_id']
        )

    def get_cartas_detalhadas(self):
        """
        Processa o texto da lista_baralho e divide linha por linha
        extraindo a quantidade e o nome de cada carta.
        
        Ignora cabeçalhos/categorias como 'Pokémon', 'Trainer', 'Energy'.
        """
        if not self.lista_baralho:
            return []

        cartas = []
        categorias = ('pokémon', 'pokemon', 'trainer', 'trainers', 'energy', 'energies')

        for linha in self.lista_baralho.strip().splitlines():
            linha = linha.strip()
            if not linha:
                continue
            
            # Normaliza a linha para checagem (remove ':' e passa para minúsculas)
            linha_limpa = linha.lower().replace(':', '').strip()

            # Se a linha começa com alguma palavra de categoria (e não com número)
            if any(linha_limpa.startswith(cat) for cat in categorias):
                partes_head = linha_limpa.split()
                # Valida se é um cabeçalho de categoria (ex: "Pokémon", "Pokémon 12", "Energy Cards")
                if len(partes_head) <= 2 or 'cards' in linha_limpa or 'cartas' in linha_limpa:
                    continue

            # Processa a quantidade e o nome da carta
            partes = linha.split(' ', 1)
            if len(partes) == 2 and partes[0].isdigit():
                quantidade = int(partes[0])
                nome_carta = partes[1].strip()
            else:
                quantidade = 1
                nome_carta = linha

            cartas.append({
                'quantidade': quantidade,
                'nome': nome_carta
            })
            
        return cartas

    def save(self):
        if self.id is None:
            with DatabaseManager() as db:
                query = "INSERT INTO decks (name, carta_principal, lista_baralho, user_id) VALUES (?, ?, ?, ?)"
                db.execute(query, (self.name, self.carta_principal, self.lista_baralho, self.user_id))
                self.id = db.cursor.lastrowid
        else:
            with DatabaseManager() as db:
                query = "UPDATE decks SET name = ?, carta_principal = ?, lista_baralho = ? WHERE id = ?"
                db.execute(query, (self.name, self.carta_principal, self.lista_baralho, self.id))
        return self

    def delete(self):
        if self.id:
            with DatabaseManager() as db:
                query = "DELETE FROM decks WHERE id = ?"
                db.execute(query, (self.id,))
            self.id = None

    @classmethod
    def get_by_user_id(cls, user_id):
        with DatabaseManager() as db:
            query = "SELECT id, name, carta_principal, lista_baralho, user_id FROM decks WHERE user_id = ?"
            db.execute(query, (user_id,))
            rows = db.fetchall()
            return [cls._from_row(row) for row in rows]

    @classmethod
    def get_by_id(cls, deck_id):
        with DatabaseManager() as db:
            query = "SELECT id, name, carta_principal, lista_baralho, user_id FROM decks WHERE id = ?"
            db.execute(query, (deck_id,))
            row = db.fetchone()
            return cls._from_row(row)