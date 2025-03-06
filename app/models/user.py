"""
Modelo de usuário
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    """Modelo de usuário do sistema"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relacionamento com o perfil
    profile = db.relationship('Profile', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Define a senha do usuário"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica a senha do usuário"""
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    """Carrega o usuário pelo ID"""
    return User.query.get(int(id)) 