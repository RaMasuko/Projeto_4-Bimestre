from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.models.deck import DeckModel

deck_bp = Blueprint('deck', __name__)

@deck_bp.route('/decks')
def index():
    decks = DeckModel.get_by_user_id(g.user.id)
    return render_template('decks.html', decks=decks)


@deck_bp.route('/decks/novo', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        carta_principal = request.form.get('carta_principal', '').strip()
        lista_baralho = request.form.get('lista_baralho', '').strip()

        if not name:
            flash("O nome do baralho é obrigatório.", "error")
            return render_template(
                'novo_deck.html', 
                name=name, 
                carta_principal=carta_principal, 
                lista_baralho=lista_baralho
            )
        else:
            novo_deck = DeckModel(
                name=name, 
                carta_principal=carta_principal, 
                lista_baralho=lista_baralho, 
                user_id=g.user.id
            )
            novo_deck.save()
            flash("Baralho criado com sucesso!", "success")
            return redirect(url_for('deck.index'))

    return render_template('novo_deck.html')


@deck_bp.route('/decks/editar/<int:deck_id>', methods=['GET', 'POST'])
def edit(deck_id):
    deck = DeckModel.get_by_id(deck_id)

    if not deck or deck.user_id != g.user.id:
        flash("Baralho não encontrado ou permissão negada.", "error")
        return redirect(url_for('deck.index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        carta_principal = request.form.get('carta_principal', '').strip()
        lista_baralho = request.form.get('lista_baralho', '').strip()

        if not name:
            flash("O nome do baralho é obrigatório.", "error")
            return render_template('editar_deck.html', deck=deck) 
        else:
            deck.name = name
            deck.carta_principal = carta_principal
            deck.lista_baralho = lista_baralho
            deck.save()
            flash("Baralho atualizado com sucesso!", "success")
            return redirect(url_for('deck.index'))

    return render_template('editar_deck.html', deck=deck)


@deck_bp.route('/decks/deletar/<int:deck_id>', methods=['POST'])
def delete(deck_id):
    deck = DeckModel.get_by_id(deck_id)

    if not deck or deck.user_id != g.user.id:
        flash("Baralho não encontrado ou permissão negada.", "error")
        return redirect(url_for('deck.index'))

    deck.delete()
    flash("Baralho excluído com sucesso!", "success")
    return redirect(url_for('deck.index'))