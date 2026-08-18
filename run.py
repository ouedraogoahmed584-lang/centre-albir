# ══════════════════════════════════════════════════════════════
# run.py — Centre Al-Bir
# Initialise la base avec tous les paramètres du site
# ══════════════════════════════════════════════════════════════

import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app, db
from app.models.user import User
from app.models.program import Program
from app.models.site_settings import SiteSettings

app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Program=Program,
                SiteSettings=SiteSettings, app=app)


def init_site_settings():
    """Initialise tous les paramètres du site dans la base de données"""

    default_settings = [
        # ── IDENTITÉ ──────────────────────────────────────────
        ('nom_centre',      'Centre Al-Bir',
         'Nom du centre',   'identite', 'text', 1),
        ('nom_complet',
         "Centre Al-Bir pour l'Enseignement du Coran et de la Sunna",
         'Nom complet officiel', 'identite', 'text', 2),
        ('nom_arabe',       'مركز البر لتعليم القرآن والسنة',
         'Nom en arabe',    'identite', 'text', 3),
        ('slogan',          "Éducation islamique d'excellence",
         'Slogan du site',  'identite', 'text', 4),
        ('slogan_arabe',    'التعليم الإسلامي المتميز',
         'Slogan en arabe', 'identite', 'text', 5),
        ('directeur',       'Cheikh Mohamed Souleimane',
         'Nom du directeur','identite', 'text', 6),
        ('annee_fondation', '2023',
         'Année de fondation', 'identite', 'text', 7),
        ('description',
         "Centre d'enseignement du Coran et de la Sunna à Ouagadougou, Burkina Faso. Nous formons des générations attachées au Livre d'Allah.",
         'Description du centre', 'identite', 'textarea', 8),
        ('citation_accueil',
         'خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ',
         'Citation affichée (arabe)', 'identite', 'text', 9),
        ('citation_source', 'Sahih Al-Bukhari',
         'Source de la citation', 'identite', 'text', 10),

        # ── CONTACT ───────────────────────────────────────────
        ('telephone1',      '+226 64 10 51 18',
         'Téléphone principal',  'contact', 'tel', 1),
        ('telephone1_raw',  '22664105118',
         'Téléphone 1 (chiffres seulement)', 'contact', 'tel', 2),
        ('telephone2',      '+226 79 01 02 32',
         'Téléphone / WhatsApp', 'contact', 'tel', 3),
        ('telephone2_raw',  '22679010232',
         'Téléphone 2 (chiffres seulement)', 'contact', 'tel', 4),
        ('email',           'centrealbir96@gmail.com',
         'Email officiel',       'contact', 'email', 5),
        ('whatsapp_lien',   'https://whatsapp.com/dl/',
         'Lien WhatsApp direct', 'contact', 'url', 6),
        ('adresse',         'Kienfangu, Ouagadougou, Burkina Faso',
         'Adresse complète',     'contact', 'text', 7),
        ('quartier',        'Kienfangu',
         'Quartier',             'contact', 'text', 8),
        ('ville',           'Ouagadougou',
         'Ville',                'contact', 'text', 9),
        ('pays',            'Burkina Faso',
         'Pays',                 'contact', 'text', 10),
        ('google_maps',
         'https://maps.app.goo.gl/F9i8TX37KXjGMNA78',
         'Lien Google Maps',     'contact', 'url', 11),
        ('horaires',        'Lundi – Samedi : 4h00 – 22h00',
         'Horaires d\'ouverture','contact', 'text', 12),
        ('facebook',        '',
         'Page Facebook',        'contact', 'url', 13),
        ('instagram',       '',
         'Compte Instagram',     'contact', 'url', 14),
        ('youtube',         '',
         'Chaîne YouTube',       'contact', 'url', 15),

        # ── ANNÉE SCOLAIRE ────────────────────────────────────
        ('annee_scolaire',  '2026 / 2027',
         'Année scolaire active', 'scolaire', 'text', 1),
        ('date_debut_inscription', '20 Août 2026',
         'Début des inscriptions', 'scolaire', 'text', 2),
        ('date_fin_inscription', '1er Octobre 2026',
         'Fin des inscriptions',   'scolaire', 'text', 3),
        ('date_debut_cours', '1er Octobre 2026',
         'Début des cours',        'scolaire', 'text', 4),
        ('date_fin_cours',  'Juillet 2027',
         'Fin des cours',          'scolaire', 'text', 5),
        ('frais_annuels',   '250 000 FCFA',
         'Frais scolaires annuels', 'scolaire', 'text', 6),
        ('tranche_age',     '15 à 50 ans',
         'Tranche d\'âge acceptée', 'scolaire', 'text', 7),

        # ── STATISTIQUES ──────────────────────────────────────
        ('stat_eleves',     '200',
         'Nombre d\'élèves inscrits', 'statistiques', 'number', 1),
        ('stat_enseignants','10',
         'Nombre d\'enseignants',     'statistiques', 'number', 2),
        ('stat_reussite',   '85%',
         'Taux de réussite',          'statistiques', 'text', 3),
        ('stat_experience', '3 ans',
         'Années d\'expérience',      'statistiques', 'text', 4),

        # ── APPARENCE ─────────────────────────────────────────
        ('couleur_principale', '#064E3B',
         'Couleur principale (vert)', 'apparence', 'color', 1),
        ('couleur_or',      '#C89B3C',
         'Couleur or',               'apparence', 'color', 2),
        ('theme_defaut',    'classic',
         'Thème par défaut',         'apparence', 'text', 3),

        # ── SEO ───────────────────────────────────────────────
        ('seo_titre',       'Centre Al-Bir — Éducation Islamique d\'Excellence | Ouagadougou',
         'Titre SEO (balise title)',  'seo', 'text', 1),
        ('seo_description',
         'Centre Al-Bir : mémorisation du Coran, Tajwid, Tafsir à Ouagadougou.',
         'Description SEO (meta)',   'seo', 'textarea', 2),
        ('url_site',        'https://centralbir.bf',
         'URL du site',             'seo', 'url', 3),
    ]

    count_added   = 0
    count_skipped = 0

    for key, value, label, category, field_type, sort_order in default_settings:
        existing = SiteSettings.query.filter_by(key=key).first()
        if not existing:
            setting = SiteSettings(
                key        = key,
                value      = value,
                label      = label,
                category   = category,
                field_type = field_type,
                sort_order = sort_order,
            )
            db.session.add(setting)
            count_added += 1
        else:
            count_skipped += 1

    db.session.commit()
    print(f'  Paramètres ajoutés  : {count_added}')
    print(f'  Paramètres existants: {count_skipped}')


@app.cli.command('init-db')
def init_db():
    """Initialise la base de données"""
    db.create_all()
    print('Base de données créée.')

    # Admin
    admin_email    = app.config['ADMIN_EMAIL']
    admin_password = app.config['ADMIN_PASSWORD']
    admin_name     = app.config['ADMIN_NAME']

    existing = User.query.filter_by(email=admin_email).first()
    if not existing:
        admin = User(
            email     = admin_email,
            full_name = admin_name,
            role      = 'admin',
            is_active = True,
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        print(f'Admin créé : {admin_email}')
    else:
        existing.set_password(admin_password)
        print(f'Admin mis à jour : {admin_email}')

    db.session.commit()

    # Programmes
    if Program.query.count() == 0:
        programmes = [
            Program(name_fr='Mémorisation du Coran (Hifz)',
                    name_ar='حفظ القرآن الكريم',
                    description_fr='Mémorisation progressive du Saint Coran.',
                    department='islamic', language='Arabe',
                    min_age=15, max_age=50, icon='📖',
                    sort_order=1, slug='memorisation-coran'),
            Program(name_fr='Tajwid (Règles de Récitation)',
                    name_ar='علم التجويد',
                    description_fr='Maîtrise des règles de récitation coranique.',
                    department='islamic', language='Arabe',
                    min_age=15, max_age=50, icon='🎤',
                    sort_order=2, slug='tajwid'),
            Program(name_fr='Tafsir du Coran',
                    name_ar='تفسير القرآن الكريم',
                    description_fr='Compréhension et interprétation du Coran.',
                    department='islamic', language='Arabe / Français',
                    min_age=15, max_age=50, icon='📚',
                    sort_order=3, slug='tafsir'),
            Program(name_fr='Mémorisation des Moutoun',
                    name_ar='حفظ المتون التأصيلية',
                    description_fr='Aqida, Fiqh, Tawhid, Sira.',
                    department='islamic', language='Arabe',
                    min_age=15, max_age=50, icon='📜',
                    sort_order=4, slug='moutoun'),
            Program(name_fr='Sciences Islamiques & Sunna',
                    name_ar='العلوم الإسلامية والسنة النبوية',
                    description_fr='Sunna, Hadiths et sciences religieuses.',
                    department='islamic', language='Arabe / Français',
                    min_age=15, max_age=50, icon='🕌',
                    sort_order=5, slug='sciences-islamiques'),
            Program(name_fr='Programme Français (CP1 – CM2)',
                    name_ar='البرنامج الفرنسي',
                    description_fr='Cycle primaire français CP1 à CM2.',
                    department='french', language='Français',
                    min_age=6, max_age=15, icon='🇫🇷',
                    sort_order=6, slug='programme-francais'),
        ]
        for p in programmes:
            db.session.add(p)
        print('6 programmes créés.')

    # Paramètres du site
    print('Initialisation des paramètres du site...')
    init_site_settings()

    db.session.commit()
    print('Initialisation terminée !')
    print(f'Email : {admin_email} | Pass : {admin_password}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
