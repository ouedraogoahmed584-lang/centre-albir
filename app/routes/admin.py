from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required
from app import db
from app.models.user import User
from app.models.student import Student
from app.models.application import Application
from app.models.program import Program
from app.models.article import Article
from app.models.gallery import Gallery
from app.models.advertisement import Advertisement
from app.models.payment import Payment
from app.models.event import Event
from app.models.teacher import Teacher
from app.utils.decorators import admin_required
from app.utils.helpers import slugify, allowed_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timezone

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'total_students':     Student.query.filter_by(status='active').count(),
        'total_teachers':     Teacher.query.filter_by(is_active=True).count(),
        'total_applications': Application.query.count(),
        'pending_applications': Application.query.filter_by(status='pending').count(),
        'total_articles':     Article.query.count(),
        'active_ads':         Advertisement.query.filter_by(is_active=True).count(),
    }
    recent_applications = Application.query.order_by(Application.submitted_at.desc()).limit(5).all()
    recent_students     = Student.query.order_by(Student.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                           stats=stats,
                           recent_applications=recent_applications,
                           recent_students=recent_students)


# ── GESTION DES INSCRIPTIONS ──────────────────────────────
@admin_bp.route('/inscriptions')
@login_required
@admin_required
def inscriptions():
    status_filter = request.args.get('status', '')
    query = Application.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    applications = query.order_by(Application.submitted_at.desc()).all()
    return render_template('admin/inscriptions.html',
                           applications=applications,
                           current_status=status_filter)


@admin_bp.route('/inscriptions/<int:id>')
@login_required
@admin_required
def inscription_detail(id):
    application = Application.query.get_or_404(id)
    programs    = Program.query.filter_by(is_active=True).all()
    return render_template('admin/inscription_detail.html',
                           application=application,
                           programs=programs)


@admin_bp.route('/inscriptions/<int:id>/statut', methods=['POST'])
@login_required
@admin_required
def update_statut(id):
    application = Application.query.get_or_404(id)
    new_status  = request.form.get('status')
    notes       = request.form.get('notes', '')
    valid_statuses = ['pending','docs_received','under_review','accepted','rejected','enrolled']
    if new_status in valid_statuses:
        application.status     = new_status
        application.admin_notes = notes
        db.session.commit()
        flash(f'Statut mis à jour : {application.status_label}', 'success')
    return redirect(url_for('admin.inscription_detail', id=id))


# ── GESTION DES ÉLÈVES ────────────────────────────────────
@admin_bp.route('/eleves')
@login_required
@admin_required
def eleves():
    students = Student.query.order_by(Student.created_at.desc()).all()
    return render_template('admin/eleves.html', students=students)


# ── GESTION DES ENSEIGNANTS ───────────────────────────────
@admin_bp.route('/enseignants')
@login_required
@admin_required
def enseignants():
    teachers = Teacher.query.order_by(Teacher.sort_order).all()
    return render_template('admin/enseignants.html', teachers=teachers)


# ── GESTION DES PROGRAMMES ────────────────────────────────
@admin_bp.route('/programmes')
@login_required
@admin_required
def programmes():
    programs = Program.query.order_by(Program.sort_order).all()
    return render_template('admin/programmes.html', programs=programs)


@admin_bp.route('/programmes/nouveau', methods=['GET', 'POST'])
@login_required
@admin_required
def nouveau_programme():
    if request.method == 'POST':
        name_fr = request.form.get('name_fr', '').strip()
        if name_fr:
            program = Program(
                name_fr        = name_fr,
                name_ar        = request.form.get('name_ar', '').strip(),
                description_fr = request.form.get('description_fr', ''),
                description_ar = request.form.get('description_ar', ''),
                objectives_fr  = request.form.get('objectives_fr', ''),
                department     = request.form.get('department', 'islamic'),
                language       = request.form.get('language', 'Arabe'),
                min_age        = int(request.form.get('min_age', 15)),
                max_age        = int(request.form.get('max_age', 50)),
                duration       = request.form.get('duration', ''),
                icon           = request.form.get('icon', '📖'),
                sort_order     = int(request.form.get('sort_order', 0)),
                slug           = slugify(name_fr),
            )
            db.session.add(program)
            db.session.commit()
            flash('Programme créé avec succès !', 'success')
            return redirect(url_for('admin.programmes'))
    return render_template('admin/programme_form.html', program=None)


# ── GESTION DES PUBLICITÉS ────────────────────────────────
@admin_bp.route('/publicites')
@login_required
@admin_required
def publicites():
    ads = Advertisement.query.order_by(Advertisement.position, Advertisement.sort_order).all()
    return render_template('admin/publicites.html', ads=ads)


@admin_bp.route('/publicites/nouvelle', methods=['GET', 'POST'])
@login_required
@admin_required
def nouvelle_publicite():
    if request.method == 'POST':
        image_url = ''
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename  = timestamp + filename
                save_path = os.path.join(current_app.root_path, 'static', 'images', 'ads', filename)
                file.save(save_path)
                image_url = f'/static/images/ads/{filename}'

        ad = Advertisement(
            title      = request.form.get('title', '').strip(),
            image_url  = image_url,
            link_url   = request.form.get('link_url', '').strip(),
            content    = request.form.get('content', '').strip(),
            position   = request.form.get('position', 'banner_top'),
            is_active  = request.form.get('is_active') == 'on',
            sort_order = int(request.form.get('sort_order', 0)),
        )
        db.session.add(ad)
        db.session.commit()
        flash('Publicité créée avec succès !', 'success')
        return redirect(url_for('admin.publicites'))
    return render_template('admin/publicite_form.html', ad=None)


@admin_bp.route('/publicites/<int:id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_publicite(id):
    ad = Advertisement.query.get_or_404(id)
    ad.is_active = not ad.is_active
    db.session.commit()
    status = 'activée' if ad.is_active else 'désactivée'
    flash(f'Publicité {status}.', 'success')
    return redirect(url_for('admin.publicites'))


@admin_bp.route('/publicites/<int:id>/supprimer', methods=['POST'])
@login_required
@admin_required
def supprimer_publicite(id):
    ad = Advertisement.query.get_or_404(id)
    db.session.delete(ad)
    db.session.commit()
    flash('Publicité supprimée.', 'success')
    return redirect(url_for('admin.publicites'))


# ── GESTION DES ACTUALITÉS ────────────────────────────────
@admin_bp.route('/actualites')
@login_required
@admin_required
def actualites():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('admin/actualites.html', articles=articles)


@admin_bp.route('/actualites/nouvelle', methods=['GET', 'POST'])
@login_required
@admin_required
def nouvel_article():
    if request.method == 'POST':
        title_fr = request.form.get('title_fr', '').strip()
        if title_fr:
            # Upload image article
            image_url = ''
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    filename  = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                    filename  = timestamp + filename
                    save_path = os.path.join(current_app.root_path, 'static', 'images', 'uploads', filename)
                    file.save(save_path)
                    image_url = f'/static/images/uploads/{filename}'

            article = Article(
                title_fr     = title_fr,
                title_ar     = request.form.get('title_ar', '').strip(),
                content_fr   = request.form.get('content_fr', ''),
                content_ar   = request.form.get('content_ar', ''),
                excerpt_fr   = request.form.get('excerpt_fr', ''),
                image_url    = image_url,
                category     = request.form.get('category', 'annonce'),
                is_pinned    = request.form.get('is_pinned') == 'on',
                slug         = slugify(title_fr),
            )
            if request.form.get('publish_now') == 'on':
                article.publish()
            db.session.add(article)
            db.session.commit()
            flash('Article créé avec succès !', 'success')
            return redirect(url_for('admin.actualites'))
    return render_template('admin/article_form.html', article=None)


# ── GESTION DE LA GALERIE ─────────────────────────────────
@admin_bp.route('/galerie')
@login_required
@admin_required
def galerie():
    photos = Gallery.query.order_by(Gallery.sort_order).all()
    return render_template('admin/galerie.html', photos=photos)


@admin_bp.route('/galerie/ajouter', methods=['POST'])
@login_required
@admin_required
def ajouter_photo():
    if 'photo' not in request.files:
        flash('Aucun fichier sélectionné.', 'danger')
        return redirect(url_for('admin.galerie'))
    file = request.files['photo']
    if file and allowed_file(file.filename):
        filename  = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename  = timestamp + filename
        save_path = os.path.join(current_app.root_path, 'static', 'images', 'uploads', filename)
        file.save(save_path)
        photo = Gallery(
            image_url  = f'/static/images/uploads/{filename}',
            caption_fr = request.form.get('caption_fr', ''),
            caption_ar = request.form.get('caption_ar', ''),
            category   = request.form.get('category', 'activite'),
            sort_order = int(request.form.get('sort_order', 0)),
        )
        db.session.add(photo)
        db.session.commit()
        flash('Photo ajoutée avec succès !', 'success')
    return redirect(url_for('admin.galerie'))


# ── PARAMÈTRES / LOGO ─────────────────────────────────────
@admin_bp.route('/parametres', methods=['GET', 'POST'])
@login_required
@admin_required
def parametres():
    if request.method == 'POST':
        # Upload du logo
        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename and allowed_file(file.filename):
                filename  = secure_filename('logo.' + file.filename.rsplit('.', 1)[1].lower())
                save_path = os.path.join(current_app.root_path, 'static', 'images', filename)
                file.save(save_path)
                flash('Logo mis à jour avec succès !', 'success')
        return redirect(url_for('admin.parametres'))
    return render_template('admin/parametres.html')


# ── GESTION DES UTILISATEURS ─────────────────────────────
@admin_bp.route('/utilisateurs')
@login_required
@admin_required
def utilisateurs():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/utilisateurs.html', users=users)
