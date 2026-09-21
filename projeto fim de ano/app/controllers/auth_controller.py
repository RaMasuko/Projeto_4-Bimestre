from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import UserModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if UserModel.verify_credentials(username, password):
            session['username'] = username
            return redirect(url_for('main.dashboard'))
        else:
            flash("Usuário ou senha inválidos.", "error")

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))