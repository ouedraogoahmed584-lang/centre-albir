from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from config import config
import os

# ── Extensions Flask ──────────────────────────────────────
db       = SQLAlchemy()
login    = LoginManager()
migrate  = Migrate()
mail     = Mail()
csrf     = CSRFProtect()


def create_app(config_name=None):
    """
    Factory pattern Flask — crée et configure l'application.
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
        if config_name == 'development':
            config_name = 'development'
        else:
            config_name = 'production'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # ── Initialisation des extensions ──────────────────────
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)

    # ── Configuration Flask-Login ──────────────────────────
    login.login_view         = 'auth.connexion'
    login.login_message      = 'Veuillez vous connecter pour accéder à cette page.'
    login.login_message_category = 'warning'

    # ── Création dossier uploads si absent ────────────────
    uploads_path = os.path.join(app.root_path, 'static', 'images', 'uploads')
    ads_path     = os.path.join(app.root_path, 'static', 'images', 'ads')
    os.makedirs(uploads_path, exist_ok=True)
    os.makedirs(ads_path, exist_ok=True)

    # ── Enregistrement des Blueprints ─────────────────────
    from app.routes.public  import public_bp
    from app.routes.auth    import auth_bp
    from app.routes.admin   import admin_bp
    from app.routes.parent  import parent_bp
    from app.routes.student import student_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp,    url_prefix='/auth')
    app.register_blueprint(admin_bp,   url_prefix='/admin')
    app.register_blueprint(parent_bp,  url_prefix='/espace/parent')
    app.register_blueprint(student_bp, url_prefix='/espace/eleve')

    # ── Contexte global pour les templates ────────────────
    from app.utils.helpers import inject_globals
    app.context_processor(inject_globals)

    # ── Import des modèles (pour Flask-Migrate) ───────────
    with app.app_context():
        from app.models import user, student, parent, teacher
        from app.models import site_settings
        from app.models import program, application, article
        from app.models import gallery, advertisement, payment
        from app.models import attendance, event

    return app
