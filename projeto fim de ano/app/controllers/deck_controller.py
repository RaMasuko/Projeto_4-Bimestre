from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app
from app.models.deck import Deck
from app.utils.auth_middleware import login_required

deck_bp = Blueprint('deck', __name__)

@deck_bp.route('/decks')
@login_required
def index():
    busca = request.args.get('busca', '').strip()
    decks = Deck.listar_por_usuario(g.usuario.id, busca=busca)
    return render_template('decks.html', decks=decks, busca=busca)


@deck_bp.route('/decks/novo', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        carta_principal = request.form.get('carta_principal', '').strip()
        lista_baralho = request.form.get('lista_baralho', '').strip()

        if not name or len(name) < 2 or len(name) > 80:
            flash("O nome do baralho é obrigatório e deve ter entre 2 e 80 caracteres.", "error")
            return render_template(
                'novo_deck.html',
                name=name,
                carta_principal=carta_principal,
                lista_baralho=lista_baralho
            )

        novo_deck = Deck(
            name=name,
            carta_principal=carta_principal,
            lista_baralho=lista_baralho,
            usuario_id=g.usuario.id
        )
        novo_deck.salvar()
        current_app.logger.info(f"Baralho '{name}' criado pelo usuário ID {g.usuario.id}")
        flash("Baralho criado com sucesso!", "success")
        return redirect(url_for('deck.index'))

    return render_template('novo_deck.html')


@deck_bp.route('/decks/<int:deck_id>/editar', methods=['GET', 'POST'])
@login_required
def edit(deck_id):
    deck = Deck.buscar_por_id(deck_id, g.usuario.id)

    if not deck:
        flash("Baralho não encontrado ou permissão negada.", "error")
        return redirect(url_for('deck.index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        carta_principal = request.form.get('carta_principal', '').strip()
        lista_baralho = request.form.get('lista_baralho', '').strip()

        if not name or len(name) < 2 or len(name) > 80:
            flash("O nome do baralho é obrigatório e deve ter entre 2 e 80 caracteres.", "error")
            return render_template('editar_deck.html', deck=deck)

        deck.name = name
        deck.carta_principal = carta_principal
        deck.lista_baralho = lista_baralho
        deck.salvar()
        current_app.logger.info(f"Baralho ID {deck.id} atualizado pelo usuário ID {g.usuario.id}")
        flash("Baralho atualizado com sucesso!", "success")
        return redirect(url_for('deck.index'))

    return render_template('editar_deck.html', deck=deck)


@deck_bp.route('/decks/<int:deck_id>/excluir', methods=['POST'])
@login_required
def delete(deck_id):
    deck = Deck.buscar_por_id(deck_id, g.usuario.id)

    if not deck:
        flash("Baralho não encontrado ou permissão negada.", "error")
        return redirect(url_for('deck.index'))

    nome_removido = deck.name
    deck.excluir()
    current_app.logger.info(f"Baralho '{nome_removido}' (ID {deck_id}) excluído pelo usuário ID {g.usuario.id}")
    flash("Baralho excluído com sucesso!", "success")
    return redirect(url_for('deck.index'))
