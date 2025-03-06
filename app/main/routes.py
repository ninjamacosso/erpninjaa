"""
Rotas principais
"""
from flask import render_template
from flask_login import current_user
from app.main import bp

@bp.route('/')
def index():
    """Página inicial"""
    return render_template('main/index.html', title='Início') 