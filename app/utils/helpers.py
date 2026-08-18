from flask import current_app
from app.models.advertisement import Advertisement
from app.models.article import Article
from app.models.event import Event
from app import db


def inject_globals():
    """
    Variables injectées dans TOUS les templates Jinja2.
    Accessible via {{ config }}, {{ ads }}, etc.
    """
    from config import config as cfg_map
    import os

    site_config = {
        'name':        'Centre Al-Bir',
        'full_name':   "Centre Al-Bir pour l'Enseignement du Coran et de la Sunna",
        'slogan':      'Éducation islamique d\'excellence',
        'director':    'Cheikh Mohamed Souleimane',
        'phone1':      '+226 64 10 51 18',
        'phone2':      '+226 79 01 02 32',
        'phone1_raw':  '22664105118',
        'phone2_raw':  '22679010232',
        'email':       'centrealbir96@gmail.com',
        'whatsapp':    'https://whatsapp.com/dl/',
        'address':     'Kienfangu, Ouagadougou, Burkina Faso',
        'maps_url':    'https://maps.app.goo.gl/F9i8TX37KXjGMNA78',
        'hours':       'Lundi – Samedi : 4h00 – 22h00',
        'school_year': '2026 / 2027',
        'enroll_start':'20 Août 2026',
        'enroll_end':  '1er Octobre 2026',
        'fee':         '250 000 FCFA',
        'age_range':   '15 à 50 ans',
        'stats': {
            'students':    200,
            'teachers':    10,
            'success_rate':'85%',
            'years':       3,
        },
        'colors': {
            'primary': '#064E3B',
            'gold':    '#C89B3C',
            'ivory':   '#FAF7F0',
        }
    }

    # Publicités actives pour le site
    try:
        active_ads = Advertisement.query.filter_by(is_active=True).all()
        ads_by_position = {}
        for ad in active_ads:
            if ad.is_currently_active:
                pos = ad.position
                if pos not in ads_by_position:
                    ads_by_position[pos] = []
                ads_by_position[pos].append(ad)
    except Exception:
        ads_by_position = {}

    return dict(
        site=site_config,
        ads=ads_by_position,
    )


def allowed_file(filename):
    """Vérifie si le fichier uploadé est autorisé"""
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png','jpg','jpeg','gif','webp','pdf'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def format_fcfa(amount):
    """Formate un montant en FCFA"""
    return f"{amount:,.0f} FCFA".replace(',', ' ')


def slugify(text):
    """Génère un slug à partir d'un texte"""
    import unicodedata, re
    text = unicodedata.normalize('NFD', text.lower())
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')
