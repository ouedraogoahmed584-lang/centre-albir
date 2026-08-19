import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db

application = create_app('production')
app = application

# Créer les tables automatiquement au démarrage
with application.app_context():
    try:
        db.create_all()
        print("[INIT] Tables créées")

        # Créer admin si absent
        from app.models.user import User
        admin_email = application.config.get('ADMIN_EMAIL', 'centrealbir96@gmail.com')
        admin_pass  = application.config.get('ADMIN_PASSWORD', '6410')
        admin_name  = application.config.get('ADMIN_NAME', 'Cheikh Mohamed Souleimane')

        if not User.query.filter_by(email=admin_email).first():
            admin = User(
                email=admin_email,
                full_name=admin_name,
                role='admin',
                is_active=True
            )
            admin.set_password(admin_pass)
            db.session.add(admin)

        # Initialiser site_settings
        try:
            from app.models.site_settings import SiteSettings
            if SiteSettings.query.count() == 0:
                from run import init_site_settings
                init_site_settings()
                print("[INIT] Settings créés")
        except Exception as e:
            print(f"[WARN] Settings: {e}")

        db.session.commit()
        print("[INIT] Base initialisée")

    except Exception as e:
        print(f"[ERROR] Init: {e}")

if __name__ == '__main__':
    application.run()
