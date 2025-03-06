"""
Inicialização da aplicação Flask
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from config import Config

# Inicialização das extensões
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

def create_app(config_class=Config):
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Configuração do login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'

    # Registrar blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/profile')

    from app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    # Criar todas as tabelas do banco de dados
    with app.app_context():
        db.create_all()

    return app

from app.models import user, profile 