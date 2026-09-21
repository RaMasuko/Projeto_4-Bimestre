import os
from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='views')

    # Configurações de segurança
    app.secret_key = os.environ.get('SECRET_KEY') or 'chave-super-secreta-mewtwo-150'
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    # Importações internas do pacote 'app'
    from app.middlewares.auth_middleware import check_auth
    from app.controllers.auth_controller import auth_bp
    from app.controllers.main_controller import main_bp

    # Aplicação do middleware global
    app.before_request(check_auth)

    # Registro dos Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app