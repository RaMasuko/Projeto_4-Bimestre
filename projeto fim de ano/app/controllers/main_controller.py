from flask import Blueprint, render_template, redirect, url_for, g, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
def dashboard():
    username = g.user.username if g.user else session.get('username', 'Treinador')
    return render_template('dashboard.html', username=username)