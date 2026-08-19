from app.utils.cache import cache_get, cache_set
from flask import Blueprint, render_template, abort
from app.models.program import Program
from app.models.article import Article
from app.models.gallery import Gallery
from app.models.event import Event
from app import db

from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from app.models.program import Program
from app.models.article import Article
from app.models.gallery import Gallery
from app.models.event import Event
from app.models.application import Application
from app import db







public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def accueil():
    programs  = Program.query.filter_by(is_active=True).order_by(Program.sort_order).all()
    articles  = Article.query.filter_by(is_published=True).order_by(Article.published_at.desc()).limit(3).all()
    gallery   = Gallery.query.filter_by(is_active=True).order_by(Gallery.sort_order).limit(6).all()
    return render_template('public/accueil.html',
                           programs=programs,
                           articles=articles,
                           gallery=gallery)


@public_bp.route('/a-propos')
def a_propos():
    return render_template('public/a_propos.html')


@public_bp.route('/programmes')
def programmes():
    programs = Program.query.filter_by(is_active=True).order_by(Program.sort_order).all()
    return render_template('public/programmes.html', programs=programs)


@public_bp.route('/programmes/<slug>')
def programme_detail(slug):
    program = Program.query.filter_by(slug=slug, is_active=True).first_or_404()
    return render_template('public/programme_detail.html', program=program)


@public_bp.route('/admissions')
def admissions():
    programs = Program.query.filter_by(is_active=True).order_by(Program.sort_order).all()
    return render_template('public/admissions.html', programs=programs)


@public_bp.route('/actualites')
def actualites():
    articles = Article.query.filter_by(is_published=True).order_by(Article.published_at.desc()).all()
    return render_template('public/actualites.html', articles=articles)


@public_bp.route('/actualites/<slug>')
def article_detail(slug):
    article = Article.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template('public/article_detail.html', article=article)


@public_bp.route('/galerie')
def galerie():
    photos = Gallery.query.filter_by(is_active=True).order_by(Gallery.sort_order).all()
    return render_template('public/galerie.html', photos=photos)


@public_bp.route('/contact')
def contact():
    return render_template('public/contact.html')


# Gestion des erreurs
@public_bp.app_errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

@public_bp.app_errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404

@public_bp.app_errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500


@public_bp.route('/admissions', methods=['POST'])
def admissions_post():
    """Traite la soumission du formulaire d'inscription"""
    import os, random, string
    from werkzeug.utils import secure_filename
    from app.utils.helpers import allowed_file
    from flask import current_app

    app_obj = Application()

    # Infos parent
    app_obj.parent_name     = request.form.get('parent_name', '').strip()
    app_obj.parent_phone    = request.form.get('parent_phone', '').strip()
    app_obj.parent_whatsapp = request.form.get('parent_whatsapp', '').strip()
    app_obj.parent_email    = request.form.get('parent_email', '').strip()

    # Infos élève
    app_obj.student_name  = request.form.get('student_name', '').strip()
    age_val = request.form.get('student_age', '0')
    app_obj.student_age   = int(age_val) if age_val.isdigit() else 0
    app_obj.student_level = request.form.get('student_level', '').strip()
    app_obj.motivation    = request.form.get('motivation', '').strip()

    prog_id = request.form.get('program_id')
    if prog_id and prog_id.isdigit():
        app_obj.program_id = int(prog_id)

    # Référence unique
    chars = string.ascii_uppercase + string.digits
    app_obj.reference = 'ALB-' + ''.join(random.choices(chars, k=8))

    # Upload documents
    upload_folder = os.path.join(current_app.root_path, 'static', 'images', 'uploads')
    for field, attr in [
        ('doc_bulletin',    'doc_bulletin_url'),
        ('doc_certificate', 'doc_certificate_url'),
        ('doc_photo',       'doc_photo_url'),
    ]:
        if field in request.files:
            file = request.files[field]
            if file and file.filename and allowed_file(file.filename):
                from datetime import datetime
                filename  = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename  = timestamp + filename
                file.save(os.path.join(upload_folder, filename))
                setattr(app_obj, attr, '/static/images/uploads/' + filename)

    db.session.add(app_obj)
    db.session.commit()

    flash(f'Votre demande a bien été envoyée ! Référence : {app_obj.reference}. Nous vous contacterons prochainement.', 'success')
    return redirect(url_for('public.admissions'))
