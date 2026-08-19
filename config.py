import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-albir-2026'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join('app', 'static', 'images', 'uploads')
    ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif','webp','svg','ico','pdf'}
    ADMIN_EMAIL    = os.environ.get('ADMIN_EMAIL',    'centrealbir96@gmail.com')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '6410')
    ADMIN_NAME     = os.environ.get('ADMIN_NAME',     'Cheikh Mohamed Souleimane')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///albir_dev.db'

class ProductionConfig(Config):
    DEBUG = False
    db_url = os.environ.get('DATABASE_URL', '')
    # Render donne postgres:// → SQLAlchemy veut postgresql://
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    # Si pas de DATABASE_URL → SQLite fallback
    if not db_url:
        db_url = 'sqlite:///albir_prod.db'
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
