from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response, current_app
from app.models.user import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    ultimo_usuario = request.cookies.get('ultimo_usuario', '')

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        lembrar = request.form.get('lembrar')

        if not username or not password:
            flash("Preencha usuário e senha.", "error")
            return render_template('login.html', ultimo_usuario=ultimo_usuario)

        user = Usuario.buscar_por_username(username)

        if user and user.verificar_senha(password):
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            current_app.logger.info(f"Login realizado com sucesso: {user.username} (ID: {user.id})")
            flash(f"Bem-vindo de volta, {user.username}!", "success")

            resp = make_response(redirect(url_for('main.dashboard')))
            if lembrar:
                resp.set_cookie('ultimo_usuario', user.username, max_age=30*24*60*60)
            else:
                resp.delete_cookie('ultimo_usuario')
            return resp
        else:
            current_app.logger.warning(f"Falha de autenticação para o usuário: {username}")
            flash("Usuário ou senha inválidos.", "error")

    return render_template('login.html', ultimo_usuario=ultimo_usuario)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not password or not confirm_password:
            flash("Preencha todos os campos obrigatórios.", "error")
        elif len(username) < 3 or len(username) > 30:
            flash("O nome de usuário deve ter entre 3 e 30 caracteres.", "error")
        elif password != confirm_password:
            flash("As senhas não coincidem.", "error")
        elif len(password) < 4:
            flash("A senha deve ter pelo menos 4 caracteres.", "error")
        elif Usuario.buscar_por_username(username):
            flash("Este nome de usuário já está em uso.", "error")
        else:
            novo_usuario = Usuario(username=username, password=password)
            novo_usuario.salvar()
            current_app.logger.info(f"Novo usuário cadastrado: {username}")
            flash("Conta criada com sucesso! Faça o login para continuar.", "success")
            return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    username = session.get('username', 'Desconhecido')
    session.clear()
    current_app.logger.info(f"Logout realizado: {username}")
    flash("Você saiu da sua conta com segurança.", "success")
    return redirect(url_for('auth.login'))
