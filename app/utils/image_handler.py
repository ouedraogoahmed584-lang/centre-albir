# ══════════════════════════════════════════════════════════════
# app/utils/image_handler.py
# Gestion centralisée des uploads d'images
# Supporte : logo, publicités, articles, galerie, enseignants
# ══════════════════════════════════════════════════════════════

import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app


# Extensions autorisées
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'ico'}


def allowed_file(filename):
    """Vérifie si l'extension du fichier est autorisée"""
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def generate_filename(original_filename, prefix=''):
    """Génère un nom de fichier unique sécurisé"""
    ext       = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    safe_name = f"{prefix}_{timestamp}_{unique_id}.{ext}" if prefix else f"{timestamp}_{unique_id}.{ext}"
    return secure_filename(safe_name)


def save_upload(file, folder_key='uploads', prefix=''):
    """
    Sauvegarde un fichier uploadé.

    Args:
        file        : FileStorage object (request.files['...'])
        folder_key  : 'uploads' | 'ads' | 'logos' | 'articles' | 'gallery' | 'teachers'
        prefix      : préfixe pour le nom du fichier

    Returns:
        str : URL relative du fichier (/static/images/...) ou None si échec
    """
    if not file or not file.filename:
        return None

    if not allowed_file(file.filename):
        return None

    # Déterminer le dossier de destination
    folder_map = {
        'uploads':  os.path.join('app', 'static', 'images', 'uploads'),
        'ads':      os.path.join('app', 'static', 'images', 'ads'),
        'logos':    os.path.join('app', 'static', 'images', 'logos'),
        'articles': os.path.join('app', 'static', 'images', 'articles'),
        'gallery':  os.path.join('app', 'static', 'images', 'gallery'),
        'teachers': os.path.join('app', 'static', 'images', 'teachers'),
    }

    folder_rel = folder_map.get(folder_key, folder_map['uploads'])

    # Chemin absolu depuis la racine du projet
    base_dir     = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    folder_abs   = os.path.join(base_dir, folder_rel)

    # Créer le dossier si absent
    os.makedirs(folder_abs, exist_ok=True)

    # Générer nom unique
    filename = generate_filename(file.filename, prefix=prefix)
    save_path = os.path.join(folder_abs, filename)

    try:
        file.save(save_path)
        # Retourner l'URL relative pour le template
        sub_folder = folder_rel.replace(os.sep, '/').replace('app/static/', '')
        return f'/static/{sub_folder}/{filename}'
    except Exception as e:
        print(f"[UPLOAD ERROR] {e}")
        return None


def save_logo(file):
    """Sauvegarde le logo du site (remplace l'existant)"""
    if not file or not file.filename:
        return None

    if not allowed_file(file.filename):
        return None

    ext      = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'png'
    filename = f'logo.{ext}'

    base_dir   = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    logos_dir  = os.path.join(base_dir, 'app', 'static', 'images', 'logos')
    images_dir = os.path.join(base_dir, 'app', 'static', 'images')

    os.makedirs(logos_dir, exist_ok=True)

    logo_path       = os.path.join(logos_dir, filename)
    logo_main_path  = os.path.join(images_dir, 'logo.png')

    try:
        file.save(logo_path)
        # Copier aussi dans images/ pour l'affichage (logo.png attendu)
        import shutil
        shutil.copy2(logo_path, logo_main_path)
        return f'/static/images/logos/{filename}'
    except Exception as e:
        print(f"[LOGO UPLOAD ERROR] {e}")
        return None
