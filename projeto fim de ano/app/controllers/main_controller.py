from flask import Blueprint, render_template, redirect, url_for, g, request, make_response, flash
from app.utils.auth_middleware import login_required
from app.models.deck import Deck
from app.models.carta_preco import CartaPreco

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if g.usuario:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    total_decks = len(Deck.listar_por_usuario(g.usuario.id))
    total_cartas = len(CartaPreco.listar_por_usuario(g.usuario.id))
    return render_template(
        'dashboard.html',
        username=g.usuario.username,
        total_decks=total_decks,
        total_cartas=total_cartas
    )

@main_bp.route('/alternar-tema', methods=['POST'])
@login_required
def alternar_tema():
    tema_atual = request.cookies.get('tema', 'escuro')
    novo_tema = 'claro' if tema_atual == 'escuro' else 'escuro'
    flash(f"Tema alterado para {novo_tema.capitalize()}!", "success")
    resp = make_response(redirect(request.referrer or url_for('main.dashboard')))
    resp.set_cookie('tema', novo_tema, max_age=30*24*60*60)
    return resp
