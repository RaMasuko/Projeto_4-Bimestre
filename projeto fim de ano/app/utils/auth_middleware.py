from functools import wraps
from flask import session, redirect, url_for, flash, g
from app.models.user import Usuario

def carregar_usuario_logado():
    """Interceptador before_request para disponibilizar g.usuario em todas as requisições."""
    user_id = session.get('user_id')
    if user_id:
        g.usuario = Usuario.buscar_por_id(user_id)
        if not g.usuario:
            session.clear()
    else:
        g.usuario = None

def login_required(f):
    """Decorator obrigatório para proteger rotas restritas validando no banco."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash("Acesso restrito. Faça login para continuar.", "error")
            return redirect(url_for('auth.login'))
        
        usuario = Usuario.buscar_por_id(user_id)
        if not usuario:
            session.clear()
            flash("Sessão inválida ou usuário não encontrado.", "error")
            return redirect(url_for('auth.login'))
        
        g.usuario = usuario
        return f(*args, **kwargs)
    return decorated_function
