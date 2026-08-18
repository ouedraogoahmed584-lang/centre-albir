# ══════════════════════════════════════════════════════════════
# app/utils/helpers.py
# Injecte les paramètres du site dans tous les templates Jinja2
# Lit depuis la base de données (table site_settings)
# L'admin modifie tout depuis le panneau — zéro code
# ══════════════════════════════════════════════════════════════

from app.utils.image_handler import allowed_file


def inject_globals():
    """
    Injecte {{ site }} et {{ ads }} dans TOUS les templates.
    Lit les données depuis la base de données.
    Fallback sur valeurs par défaut si DB inaccessible.
    """
    from app.models.advertisement import Advertisement

    # Lire les paramètres depuis la base de données
    try:
        from app.models.site_settings import SiteSettings
        s = SiteSettings.get_dict()
    except Exception:
        s = {}

    # Construire le dictionnaire site avec fallback
    def g(key, default=''):
        return s.get(key, default) or default

    site_config = {
        # Identité
        'name':         g('nom_centre',   'Centre Al-Bir'),
        'full_name':    g('nom_complet',  "Centre Al-Bir pour l'Enseignement du Coran et de la Sunna"),
        'name_ar':      g('nom_arabe',    'مركز البر لتعليم القرآن والسنة'),
        'slogan':       g('slogan',       "Éducation islamique d'excellence"),
        'slogan_ar':    g('slogan_arabe', 'التعليم الإسلامي المتميز'),
        'director':     g('directeur',   'Cheikh Mohamed Souleimane'),
        'founded':      g('annee_fondation', '2023'),
        'description':  g('description', ''),
        'citation':     g('citation_accueil', 'خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ'),
        'citation_src': g('citation_source', 'Sahih Al-Bukhari'),

        # Contact
        'phone1':       g('telephone1',     '+226 64 10 51 18'),
        'phone2':       g('telephone2',     '+226 79 01 02 32'),
        'phone1_raw':   g('telephone1_raw', '22664105118'),
        'phone2_raw':   g('telephone2_raw', '22679010232'),
        'email':        g('email',          'centrealbir96@gmail.com'),
        'whatsapp':     g('whatsapp_lien',  'https://whatsapp.com/dl/'),
        'address':      g('adresse',        'Kienfangu, Ouagadougou, Burkina Faso'),
        'quartier':     g('quartier',       'Kienfangu'),
        'city':         g('ville',          'Ouagadougou'),
        'country':      g('pays',           'Burkina Faso'),
        'maps_url':     g('google_maps',    'https://maps.app.goo.gl/F9i8TX37KXjGMNA78'),
        'hours':        g('horaires',       'Lundi – Samedi : 4h00 – 22h00'),
        'facebook':     g('facebook',       ''),
        'instagram':    g('instagram',      ''),
        'youtube':      g('youtube',        ''),

        # Scolaire
        'school_year':  g('annee_scolaire',          '2026 / 2027'),
        'enroll_start': g('date_debut_inscription',   '20 Août 2026'),
        'enroll_end':   g('date_fin_inscription',     '1er Octobre 2026'),
        'course_start': g('date_debut_cours',         '1er Octobre 2026'),
        'course_end':   g('date_fin_cours',           'Juillet 2027'),
        'fee':          g('frais_annuels',            '250 000 FCFA'),
        'age_range':    g('tranche_age',              '15 à 50 ans'),

        # Statistiques
        'stats': {
            'students':     g('stat_eleves',      '200'),
            'teachers':     g('stat_enseignants', '10'),
            'success_rate': g('stat_reussite',    '85%'),
            'years':        g('stat_experience',  '3 ans'),
        },

        # Apparence
        'colors': {
            'primary': g('couleur_principale', '#064E3B'),
            'gold':    g('couleur_or',         '#C89B3C'),
        },

        # SEO
        'seo_title': g('seo_titre',       ''),
        'seo_desc':  g('seo_description', ''),
        'site_url':  g('url_site',        'https://centralbir.bf'),
    }

    # Publicités actives par position
    try:
        active_ads = Advertisement.query.filter_by(is_active=True).all()
        ads_by_pos = {}
        for ad in active_ads:
            if ad.is_currently_active:
                if ad.position not in ads_by_pos:
                    ads_by_pos[ad.position] = []
                ads_by_pos[ad.position].append(ad)
    except Exception:
        ads_by_pos = {}

    return dict(site=site_config, ads=ads_by_pos)


def format_fcfa(amount):
    """Formate un montant en FCFA"""
    return f"{amount:,.0f} FCFA".replace(',', ' ')


def slugify(text):
    """Génère un slug URL depuis un texte"""
    import unicodedata
    import re
    text = unicodedata.normalize('NFD', str(text).lower())
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')
