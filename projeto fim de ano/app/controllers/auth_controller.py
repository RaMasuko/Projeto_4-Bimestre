from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import UserModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = UserModel.get_by_username(username)

        if user and user.check_password(password):
            session['username'] = user.username
            return redirect(url_for('main.dashboard'))
        else:
            flash("Usuário ou senha inválidos.", "error")

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not password or not confirm_password:
            flash("Preencha todos os campos obrigatórios.", "error")
        elif password != confirm_password:
            flash("As senhas não coincidem.", "error")
        elif len(password) < 4:
            flash("A senha deve ter pelo menos 4 caracteres.", "error")
        elif UserModel.get_by_username(username):
            flash("Este nome de usuário já está em uso.", "error")
        else:
            UserModel.create(username, password)
            flash("Conta criada com sucesso! Faça o login para continuar.", "success")
            return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))