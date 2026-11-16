from app.db import DatabaseConnection

class CartaPreco:
    def __init__(self, nome_carta, colecao, raridade, preco_estimado, usuario_id=None, id=None):
        self.id = id
        self.nome_carta = nome_carta
        self.colecao = colecao
        self.raridade = raridade
        self.preco_estimado = float(preco_estimado)
        self.usuario_id = usuario_id

    @classmethod
    def _from_row(cls, row):
        if not row:
            return None
        return cls(
            id=row['id'],
            nome_carta=row['nome_carta'],
            colecao=row['colecao'],
            raridade=row['raridade'],
            preco_estimado=row['preco_estimado'],
            usuario_id=row['usuario_id']
        )

    def salvar(self):
        if self.id is None:
            with DatabaseConnection() as db:
                sql = "INSERT INTO cartas_precos (nome_carta, colecao, raridade, preco_estimado, usuario_id) VALUES (?, ?, ?, ?, ?)"
                db.cursor.execute(sql, (self.nome_carta, self.colecao, self.raridade, self.preco_estimado, self.usuario_id))
                self.id = db.cursor.lastrowid
        else:
            with DatabaseConnection() as db:
                sql = "UPDATE cartas_precos SET nome_carta = ?, colecao = ?, raridade = ?, preco_estimado = ? WHERE id = ? AND usuario_id = ?"
                db.cursor.execute(sql, (self.nome_carta, self.colecao, self.raridade, self.preco_estimado, self.id, self.usuario_id))
        return self

    def excluir(self):
        if self.id and self.usuario_id:
            with DatabaseConnection() as db:
                sql = "DELETE FROM cartas_precos WHERE id = ? AND usuario_id = ?"
                db.cursor.execute(sql, (self.id, self.usuario_id))
            self.id = None

    @classmethod
    def listar_por_usuario(cls, usuario_id, busca=''):
        with DatabaseConnection() as db:
            if busca:
                sql = "SELECT id, nome_carta, colecao, raridade, preco_estimado, usuario_id FROM cartas_precos WHERE usuario_id = ? AND (nome_carta LIKE ? OR colecao LIKE ?) ORDER BY id DESC"
                termo = f"%{busca}%"
                db.cursor.execute(sql, (usuario_id, termo, termo))
            else:
                sql = "SELECT id, nome_carta, colecao, raridade, preco_estimado, usuario_id FROM cartas_precos WHERE usuario_id = ? ORDER BY id DESC"
                db.cursor.execute(sql, (usuario_id,))
            rows = db.cursor.fetchall()
            return [cls._from_row(row) for row in rows]

    @classmethod
    def buscar_por_id(cls, carta_id, usuario_id):
        with DatabaseConnection() as db:
            sql = "SELECT id, nome_carta, colecao, raridade, preco_estimado, usuario_id FROM cartas_precos WHERE id = ? AND usuario_id = ?"
            db.cursor.execute(sql, (carta_id, usuario_id))
            row = db.cursor.fetchone()
            return cls._from_row(row)
