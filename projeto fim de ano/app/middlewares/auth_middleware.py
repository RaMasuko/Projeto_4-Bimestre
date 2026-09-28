from flask import session, redirect, url_for, flash, request

def check_auth():
    # Incluído 'auth.register' nas rotas públicas
    public_endpoints = ['auth.login', 'auth.register', 'main.index', 'static']
    
    if request.endpoint and request.endpoint not in public_endpoints:
        if 'username' not in session:
            flash("Acesso negado. Por favor, faça o login primeiro.", "error")
            return redirect(url_for('auth.login'))