import os
import logging
from flask import Flask, render_template, request

def create_app():
    app = Flask(__name__, template_folder='views')

    app.secret_key = os.environ.get('SECRET_KEY') or 'chave-super-secreta-mewtwo-150'
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    from app.utils.auth_middleware import carregar_usuario_logado
    from app.controllers.auth_controller import auth_bp
    from app.controllers.main_controller import main_bp
    from app.controllers.deck_controller import deck_bp
    from app.controllers.carta_controller import carta_bp

    app.before_request(carregar_usuario_logado)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(deck_bp)
    app.register_blueprint(carta_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.warning(f"Erro 404 - Página não encontrada: {request.path}")
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error(f"Erro 500 - Falha interna do servidor: {e}")
        return render_template('404.html', erro_500=True), 500

    return app
