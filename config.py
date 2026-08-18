import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration de base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-a-changer-en-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'app/static/images/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf'}

    MAIL_SERVER   = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT     = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS  = os.environ.get('MAIL_USE_TLS', '1') == '1'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')

    ADMIN_EMAIL    = os.environ.get('ADMIN_EMAIL', 'centrealbir96@gmail.com')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin2026@AlBir')
    ADMIN_NAME     = os.environ.get('ADMIN_NAME', 'Cheikh Mohamed Souleimane')


class DevelopmentConfig(Config):
    """Configuration développement local"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///albir_dev.db'
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    """Configuration production (Render)"""
    DEBUG = False
    db_url = os.environ.get('DATABASE_URL', '')
    # Render fournit postgresql:// mais SQLAlchemy veut postgresql+psycopg2://
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql+psycopg2://', 1)
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Configuration tests"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'testing':     TestingConfig,
    'default':     DevelopmentConfig,
}
