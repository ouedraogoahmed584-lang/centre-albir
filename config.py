# ══════════════════════════════════════════════════════════════
# config.py — Configuration Centre Al-Bir
# Upload : 32MB max, tous formats images acceptés
# ══════════════════════════════════════════════════════════════

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration de base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-centre-albir-2026'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload — 32 MB maximum
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024

    # Extensions autorisées
    ALLOWED_EXTENSIONS = {
        'png', 'jpg', 'jpeg', 'gif', 'webp',
        'svg', 'ico', 'pdf'
    }

    # Dossiers d'upload (chemins relatifs depuis app/)
    UPLOAD_FOLDER     = os.path.join('app', 'static', 'images', 'uploads')
    ADS_FOLDER        = os.path.join('app', 'static', 'images', 'ads')
    LOGOS_FOLDER      = os.path.join('app', 'static', 'images', 'logos')
    ARTICLES_FOLDER   = os.path.join('app', 'static', 'images', 'articles')
    GALLERY_FOLDER    = os.path.join('app', 'static', 'images', 'gallery')
    TEACHERS_FOLDER   = os.path.join('app', 'static', 'images', 'teachers')

    # Mail
    MAIL_SERVER   = os.environ.get('MAIL_SERVER',   'smtp.gmail.com')
    MAIL_PORT     = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS  = os.environ.get('MAIL_USE_TLS',  '1') == '1'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Admin par défaut
    ADMIN_EMAIL    = os.environ.get('ADMIN_EMAIL',    'centrealbir96@gmail.com')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '6410')
    ADMIN_NAME     = os.environ.get('ADMIN_NAME',     'Cheikh Mohamed Souleimane')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or 'sqlite:///albir_dev.db'
    )


class ProductionConfig(Config):
    DEBUG = False
    db_url = os.environ.get('DATABASE_URL', '')
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql+psycopg2://', 1)
    SQLALCHEMY_DATABASE_URI = db_url


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'testing':     TestingConfig,
    'default':     DevelopmentConfig,
}
