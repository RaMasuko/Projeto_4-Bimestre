from flask import session, redirect, url_for, flash, request, g
from app.models.user import UserModel

def check_auth():
    """Middleware executado antes de cada requisição (before_request)."""
    # 1. Recupera o usuário da sessão (se existir) e injeta no contexto global 'g'
    username = session.get('username')
    g.user = UserModel.get_by_username(username) if username else None

    # 2. Define endpoints públicos
    public_endpoints = ['auth.login', 'auth.register', 'main.index', 'static']
    
    # 3. Protege rotas privadas automaticamente
    if request.endpoint and request.endpoint not in public_endpoints:
        if not g.user:
            flash("Acesso negado. Por favor, faça o login primeiro.", "error")
            return redirect(url_for('auth.login'))