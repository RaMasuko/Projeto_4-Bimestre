from app.database import DatabaseManager

class DeckModel:
    def __init__(self, name, carta_principal=None, user_id=None, id=None):
        self.id = id
        self.name = name
        self.carta_principal = carta_principal
        self.user_id = user_id

    @classmethod
    def _from_row(cls, row):
        if not row:
            return None
        return cls(
            id=row['id'],
            name=row['name'],
            carta_principal=row['carta_principal'],
            user_id=row['user_id']
        )

    def save(self):
        if self.id is None:
            with DatabaseManager() as db:
                query = "INSERT INTO decks (name, carta_principal, user_id) VALUES (?, ?, ?)"
                db.execute(query, (self.name, self.carta_principal, self.user_id))
                self.id = db.cursor.lastrowid
        else:
            with DatabaseManager() as db:
                query = "UPDATE decks SET name = ?, carta_principal = ? WHERE id = ?"
                db.execute(query, (self.name, self.carta_principal, self.id))
        return self

    def delete(self):
        """[ACTIVE RECORD] Remove o registro do banco de dados."""
        if self.id:
            with DatabaseManager() as db:
                query = "DELETE FROM decks WHERE id = ?"
                db.execute(query, (self.id,))
            self.id = None

    @classmethod
    def get_by_user_id(cls, user_id):
        with DatabaseManager() as db:
            query = "SELECT id, name, carta_principal, user_id FROM decks WHERE user_id = ?"
            db.execute(query, (user_id,))
            rows = db.fetchall()
            return [cls._from_row(row) for row in rows]

    @classmethod
    def get_by_id(cls, deck_id):
        """Busca um baralho específico pelo ID."""
        with DatabaseManager() as db:
            query = "SELECT id, name, carta_principal, user_id FROM decks WHERE id = ?"
            db.execute(query, (deck_id,))
            row = db.fetchone()
            return cls._from_row(row)