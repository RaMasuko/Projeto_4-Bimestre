from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.deck import DeckModel
from app.models.user import UserModel

deck_bp = Blueprint('deck', __name__)

@deck_bp.route('/decks')
def index():
    user = UserModel.get_by_username(session.get('username'))
    if not user:
        return redirect(url_for('auth.login'))
    
    decks = DeckModel.get_by_user_id(user.id)
    return render_template('decks.html', decks=decks)

@deck_bp.route('/decks/novo', methods=['GET', 'POST'])
def create():
    user = UserModel.get_by_username(session.get('username'))
    if not user:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        carta_principal = request.form.get('carta_principal', '').strip()

        if not name:
            flash("O nome do baralho é obrigatório.", "error")
        else:
            novo_deck = DeckModel(name=name, carta_principal=carta_principal, user_id=user.id)
            novo_deck.save()
            flash("Baralho criado com sucesso!", "success")
            return redirect(url_for('deck.index'))

    return render_template('novo_deck.html')

@deck_bp.route('/decks/deletar/<int:deck_id>', methods=['POST'])
def delete(deck_id):
    user = UserModel.get_by_username(session.get('username'))
    if not user:
        return redirect(url_for('auth.login'))

    deck = DeckModel.get_by_id(deck_id)

    # Valida se o baralho existe e se pertence ao usuário logado
    if not deck or deck.user_id != user.id:
        flash("Baralho não encontrado ou permissão negada.", "error")
        return redirect(url_for('deck.index'))

    # Executa a remoção via Active Record
    deck.delete()
    flash("Baralho excluído com sucesso!", "success")
    return redirect(url_for('deck.index'))