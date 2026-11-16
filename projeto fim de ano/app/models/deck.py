from app.db import DatabaseConnection

class Deck:
    def __init__(self, name, carta_principal=None, lista_baralho=None, usuario_id=None, id=None):
        self.id = id
        self.name = name
        self.carta_principal = carta_principal
        self.lista_baralho = lista_baralho
        self.usuario_id = usuario_id

    @classmethod
    def _from_row(cls, row):
        if not row:
            return None
        return cls(
            id=row['id'],
            name=row['name'],
            carta_principal=row['carta_principal'],
            lista_baralho=row['lista_baralho'],
            usuario_id=row['usuario_id']
        )

    def get_cartas_detalhadas(self):
        if not self.lista_baralho:
            return []

        cartas = []
        categorias = ('pokémon', 'pokemon', 'trainer', 'trainers', 'energy', 'energies')

        for linha in self.lista_baralho.strip().splitlines():
            linha = linha.strip()
            if not linha:
                continue
            linha_limpa = linha.lower().replace(':', '').strip()
            if any(linha_limpa.startswith(cat) for cat in categorias):
                partes_head = linha_limpa.split()
                if len(partes_head) <= 2 or 'cards' in linha_limpa or 'cartas' in linha_limpa:
                    continue

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

    def salvar(self):
        if self.id is None:
            with DatabaseConnection() as db:
                sql = "INSERT INTO decks (name, carta_principal, lista_baralho, usuario_id) VALUES (?, ?, ?, ?)"
                db.cursor.execute(sql, (self.name, self.carta_principal, self.lista_baralho, self.usuario_id))
                self.id = db.cursor.lastrowid
        else:
            with DatabaseConnection() as db:
                sql = "UPDATE decks SET name = ?, carta_principal = ?, lista_baralho = ? WHERE id = ? AND usuario_id = ?"
                db.cursor.execute(sql, (self.name, self.carta_principal, self.lista_baralho, self.id, self.usuario_id))
        return self

    def excluir(self):
        if self.id and self.usuario_id:
            with DatabaseConnection() as db:
                sql = "DELETE FROM decks WHERE id = ? AND usuario_id = ?"
                db.cursor.execute(sql, (self.id, self.usuario_id))
            self.id = None

    @classmethod
    def listar_por_usuario(cls, usuario_id, busca=''):
        with DatabaseConnection() as db:
            if busca:
                sql = "SELECT id, name, carta_principal, lista_baralho, usuario_id FROM decks WHERE usuario_id = ? AND (name LIKE ? OR carta_principal LIKE ?) ORDER BY id DESC"
                termo = f"%{busca}%"
                db.cursor.execute(sql, (usuario_id, termo, termo))
            else:
                sql = "SELECT id, name, carta_principal, lista_baralho, usuario_id FROM decks WHERE usuario_id = ? ORDER BY id DESC"
                db.cursor.execute(sql, (usuario_id,))
            rows = db.cursor.fetchall()
            return [cls._from_row(row) for row in rows]

    @classmethod
    def buscar_por_id(cls, deck_id, usuario_id):
        with DatabaseConnection() as db:
            sql = "SELECT id, name, carta_principal, lista_baralho, usuario_id FROM decks WHERE id = ? AND usuario_id = ?"
            db.cursor.execute(sql, (deck_id, usuario_id))
            row = db.cursor.fetchone()
            return cls._from_row(row)
