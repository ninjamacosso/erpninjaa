"""
Configurações da aplicação
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    """Configurações base"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///erp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload de arquivos
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'app/static/uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 25))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'false').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # Cache
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0') 