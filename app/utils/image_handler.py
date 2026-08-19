# ══════════════════════════════════════════════════════
# app/utils/image_handler.py — Version optimisée
# Compression automatique + WebP + resize
# ══════════════════════════════════════════════════════
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'ico'}
MAX_WIDTH  = 1200  # pixels max
MAX_HEIGHT = 1200
QUALITY    = 82    # qualité WebP/JPEG (82% = bon compromis)


def allowed_file(filename):
    if not filename or '.' not in filename:
        return False
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def compress_and_save(file, save_path, max_w=MAX_WIDTH, max_h=MAX_HEIGHT):
    """
    Compresse et sauvegarde une image.
    Convertit en WebP si possible.
    Réduit si trop grande.
    """
    try:
        from PIL import Image
        import io

        img = Image.open(file)

        # Convertir RGBA → RGB si nécessaire (pour JPEG/WebP)
        if img.mode in ('RGBA', 'P', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if img.mode in ('RGBA', 'LA'):
                background.paste(img, mask=img.split()[-1])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Redimensionner si trop grande
        w, h = img.size
        if w > max_w or h > max_h:
            img.thumbnail((max_w, max_h), Image.LANCZOS)

        # Sauvegarder en WebP (plus léger)
        webp_path = save_path.rsplit('.', 1)[0] + '.webp'
        img.save(webp_path, 'WebP', quality=QUALITY, optimize=True)
        return webp_path

    except Exception as e:
        print(f"[COMPRESS] Erreur: {e} — sauvegarde originale")
        try:
            file.seek(0)
            with open(save_path, 'wb') as f:
                f.write(file.read())
            return save_path
        except Exception:
            return None


def save_upload(file, folder_key='uploads', prefix=''):
    if not file or not file.filename:
        return None
    if not allowed_file(file.filename):
        return None

    folder_map = {
        'uploads':  os.path.join('app', 'static', 'images', 'uploads'),
        'ads':      os.path.join('app', 'static', 'images', 'ads'),
        'logos':    os.path.join('app', 'static', 'images', 'logos'),
        'articles': os.path.join('app', 'static', 'images', 'articles'),
        'gallery':  os.path.join('app', 'static', 'images', 'gallery'),
        'teachers': os.path.join('app', 'static', 'images', 'teachers'),
    }

    folder_rel = folder_map.get(folder_key, folder_map['uploads'])
    base_dir   = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    folder_abs = os.path.join(base_dir, folder_rel)
    os.makedirs(folder_abs, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    ext       = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
    base_name = f"{prefix}_{timestamp}_{unique_id}.{ext}" if prefix else f"{timestamp}_{unique_id}.{ext}"
    save_path = os.path.join(folder_abs, secure_filename(base_name))

    # Compresser et sauvegarder
    final_path = compress_and_save(file, save_path)
    if not final_path:
        return None

    final_name = os.path.basename(final_path)
    sub_folder = folder_rel.replace(os.sep, '/').replace('app/static/', '')
    return f'/static/{sub_folder}/{final_name}'


def save_logo(file):
    if not file or not file.filename:
        return None
    if not allowed_file(file.filename):
        return None

    base_dir  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    logos_dir = os.path.join(base_dir, 'app', 'static', 'images', 'logos')
    imgs_dir  = os.path.join(base_dir, 'app', 'static', 'images')
    os.makedirs(logos_dir, exist_ok=True)

    save_path = os.path.join(logos_dir, 'logo_original.jpg')
    final_path = compress_and_save(file, save_path, max_w=512, max_h=512)

    if final_path:
        import shutil
        logo_main = os.path.join(imgs_dir, 'logo.webp')
        shutil.copy2(final_path, logo_main)
        # Aussi en PNG pour compatibilité
        try:
            from PIL import Image
            img = Image.open(final_path)
            img.save(os.path.join(imgs_dir, 'logo.png'), 'PNG', optimize=True)
        except Exception:
            pass
        return f'/static/images/logo.webp'
    return None
