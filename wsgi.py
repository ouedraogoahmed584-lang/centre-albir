import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import (user, student, parent, teacher,
                        program, application, article,
                        gallery, advertisement, payment,
                        attendance, event)
from app.models.site_settings import SiteSettings

application = create_app('production')
app = application

# INIT BASE DE DONNÉES AU DÉMARRAGE
with application.app_context():
    db.create_all()
    print("[OK] Tables créées")

    from app.models.user import User
    admin_email = application.config.get('ADMIN_EMAIL', 'centrealbir96@gmail.com')
    if not User.query.filter_by(email=admin_email).first():
        admin = User(
            email=admin_email,
            full_name=application.config.get('ADMIN_NAME', 'Cheikh Mohamed Souleimane'),
            role='admin',
            is_active=True
        )
        admin.set_password(application.config.get('ADMIN_PASSWORD', '6410'))
        db.session.add(admin)

    from app.models.program import Program
    if Program.query.count() == 0:
        programmes = [
            Program(name_fr='Mémorisation du Coran (Hifz)',
                    name_ar='حفظ القرآن الكريم',
                    description_fr='Mémorisation progressive du Saint Coran.',
                    department='islamic', language='Arabe',
                    min_age=15, max_age=50, icon='📖',
                    sort_order=1, slug='memorisation-coran'),
            Program(name_fr='Tajwid',
                    name_ar='علم التجويد',
                    description_fr='Règles de récitation coranique.',
                    department='islamic', language='Arabe',
                    min_age=15, max_age=50, icon='🎤',
                    sort_order=2, slug='tajwid'),
            Program(name_fr='Tafsir du Coran',
                    name_ar='تفسير القرآن الكريم',
                    description_fr='Compréhension du Coran.',
                    department='islamic', language='Arabe / Français',
                    min_age=15, max_age=50, icon='📚',
                    sort_order=3, slug='tafsir'),
            Program(name_fr='Mémorisation des Moutoun',
                    name_ar='حفظ المتون',
                    description_fr='Aqida, Fiqh, Tawhid, Sira.',
                    department='islamic', language='Arabe',
                    min_age=15, max_age=50, icon='📜',
                    sort_order=4, slug='moutoun'),
            Program(name_fr='Sciences Islamiques & Sunna',
                    name_ar='العلوم الإسلامية',
                    description_fr='Sunna et sciences religieuses.',
                    department='islamic', language='Arabe / Français',
                    min_age=15, max_age=50, icon='🕌',
                    sort_order=5, slug='sciences-islamiques'),
            Program(name_fr='Programme Français CP1-CM2',
                    name_ar='البرنامج الفرنسي',
                    description_fr='Cycle primaire français.',
                    department='french', language='Français',
                    min_age=6, max_age=15, icon='🇫🇷',
                    sort_order=6, slug='programme-francais'),
        ]
        for p in programmes:
            db.session.add(p)
        print("[OK] Programmes créés")

    if SiteSettings.query.count() == 0:
        from run import init_site_settings
        try:
            init_site_settings()
            print("[OK] Settings créés")
        except Exception as e:
            print(f"[WARN] {e}")

    db.session.commit()
    print("[OK] Base initialisée avec succès")

if __name__ == '__main__':
    application.run()

# KEEP-ALIVE : Éviter la dormance du plan gratuit Render
import threading
import urllib.request
import os

def keep_alive():
    """Ping le site toutes les 14 minutes pour éviter la dormance"""
    import time
    url = os.environ.get('RENDER_EXTERNAL_URL', '')
    if not url:
        return
    while True:
        time.sleep(840)  # 14 minutes
        try:
            urllib.request.urlopen(url + '/health', timeout=10)
            print("[KEEP-ALIVE] Ping OK")
        except Exception:
            pass

# Route santé
@application.route('/health')
def health():
    from flask import jsonify
    return jsonify({'status': 'ok', 'app': 'Centre Al-Bir'})

# Lancer keep-alive en arrière-plan
if os.environ.get('FLASK_ENV') == 'production':
    t = threading.Thread(target=keep_alive, daemon=True)
    t.start()