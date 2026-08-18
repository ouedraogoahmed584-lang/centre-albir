import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app, db
from app.models.user import User
from app.models.program import Program

app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Program=Program, app=app)


@app.cli.command('init-db')
def init_db():
    """Initialise la base de données et crée l'admin par défaut."""
    db.create_all()
    print('Base de données créée.')

    # Créer admin si absent
    admin_email = app.config['ADMIN_EMAIL']
    if not User.query.filter_by(email=admin_email).first():
        admin = User(
            email     = admin_email,
            full_name = app.config['ADMIN_NAME'],
            role      = 'admin',
            is_active = True,
        )
        admin.set_password(app.config['ADMIN_PASSWORD'])
        db.session.add(admin)

    # Créer les programmes par défaut
    if Program.query.count() == 0:
        programmes_defaut = [
            Program(name_fr='Mémorisation du Coran (Hifz)',
                    name_ar='حفظ القرآن الكريم',
                    description_fr="Mémorisation progressive du Saint Coran, lettre par lettre, avec révision régulière.",
                    department='islamic', language='Arabe',
                    min_age=15, max_age=50, icon='📖',
                    sort_order=1, slug='memorisation-coran'),
            Program(name_fr='Tajwid (Règles de Récitation)',
                    name_ar='علم التجويد',
                    description_fr="Maîtrise des règles de prononciation et de récitation coranique.",
                    department='islamic', language='Arabe',
                    min_age=15, max_age=50, icon='🎤',
                    sort_order=2, slug='tajwid'),
            Program(name_fr='Tafsir du Coran',
                    name_ar='تفسير القرآن الكريم',
                    description_fr="Compréhension et interprétation du Saint Coran.",
                    department='islamic', language='Arabe / Français',
                    min_age=15, max_age=50, icon='📚',
                    sort_order=3, slug='tafsir'),
            Program(name_fr='Mémorisation des Moutoun',
                    name_ar='حفظ المتون التأصيلية',
                    description_fr="Mémorisation des textes fondamentaux : Aqida, Fiqh, Tawhid, Sira.",
                    department='islamic', language='Arabe',
                    min_age=15, max_age=50, icon='📜',
                    sort_order=4, slug='moutoun'),
            Program(name_fr='Sciences Islamiques & Sunna',
                    name_ar='العلوم الإسلامية والسنة النبوية',
                    description_fr="Étude de la Sunna, des Hadiths et des sciences religieuses.",
                    department='islamic', language='Arabe / Français',
                    min_age=15, max_age=50, icon='🕌',
                    sort_order=5, slug='sciences-islamiques'),
            Program(name_fr='Programme Français (CP1 – CM2)',
                    name_ar='البرنامج الفرنسي',
                    description_fr="Formation académique du cycle primaire en français, du CP1 au CM2.",
                    department='french', language='Français',
                    min_age=6, max_age=15, icon='🇫🇷',
                    sort_order=6, slug='programme-francais'),
        ]
        for p in programmes_defaut:
            db.session.add(p)

    db.session.commit()
    print(f'Admin créé : {admin_email}')
    print('6 programmes créés.')
    print('Initialisation terminée !')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
