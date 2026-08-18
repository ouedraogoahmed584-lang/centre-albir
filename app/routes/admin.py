# ══════════════════════════════════════════════════════════════
# IMPORTS admin.py — version corrigée avec tous les imports
# current_user était manquant → crash sur toggle_user
# ══════════════════════════════════════════════════════════════
from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, jsonify, current_app)
from flask_login import login_required, current_user
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
from app.models.site_settings import SiteSettings
from app.utils.decorators import admin_required
from app.utils.helpers import slugify, allowed_file
from app.utils.image_handler import save_upload, save_logo
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timezone

admin_bp = Blueprint('admin', __name__)

# ── TABLEAU DE BORD ─────────────────────────────────────────
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'total_students':      Student.query.filter_by(status='active').count(),
        'total_teachers':      Teacher.query.filter_by(is_active=True).count(),
        'total_applications':  Application.query.count(),
        'pending_applications': Application.query.filter_by(status='pending').count(),
        'total_articles':      Article.query.count(),
        'active_ads':          Advertisement.query.filter_by(is_active=True).count(),
    }
    recent_applications = Application.query.order_by(Application.submitted_at.desc()).limit(5).all()
    recent_students     = Student.query.order_by(Student.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                           stats=stats,
                           recent_applications=recent_applications,
                           recent_students=recent_students)

# ── GESTION DES INSCRIPTIONS ─────────────────────────────────
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
        application.status      = new_status
        application.admin_notes = notes
        db.session.commit()
        flash(f'Statut mis à jour : {application.status_label}', 'success')
    return redirect(url_for('admin.inscription_detail', id=id))

# ── GESTION DES ÉLÈVES ───────────────────────────────────────
@admin_bp.route('/eleves')
@login_required
@admin_required
def eleves():
    students = Student.query.order_by(Student.created_at.desc()).all()
    return render_template('admin/eleves.html', students=students)

@admin_bp.route('/eleves/<int:id>')
@login_required
@admin_required
def eleve_detail(id):
    """Détail d'un élève"""
    student = Student.query.get_or_404(id)
    return render_template('admin/eleve_detail.html', student=student)

# ── GESTION DES ENSEIGNANTS ─────────────────────────────────
@admin_bp.route('/enseignants')
@login_required
@admin_required
def enseignants():
    teachers = Teacher.query.order_by(Teacher.sort_order).all()
    return render_template('admin/enseignants.html', teachers=teachers)

@admin_bp.route('/enseignants/nouveau', methods=['GET', 'POST'])
@login_required
@admin_required
def nouvel_enseignant():
    """Formulaire et traitement d'ajout d'enseignant"""
    if request.method == 'POST':
        teacher = Teacher(
            full_name     = request.form.get('full_name', '').strip(),
            speciality    = request.form.get('speciality', '').strip(),
            qualification = request.form.get('qualification', '').strip(),
            phone         = request.form.get('phone', '').strip(),
            is_active     = True,
            show_on_site  = request.form.get('show_on_site') == 'on',
        )
        db.session.add(teacher)
        db.session.commit()
        flash('Enseignant ajouté avec succès !', 'success')
        return redirect(url_for('admin.enseignants'))
    return render_template('admin/enseignant_form.html')

# ── GESTION DES PROGRAMMES ───────────────────────────────────
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

# ── GESTION DES PUBLICITÉS ───────────────────────────────────
@admin_bp.route('/publicites')
@login_required
@admin_required
def publicites():
    ads = Advertisement.query.order_by(Advertisement.position, Advertisement.sort_order).all()
    return render_template('admin/publicites.html', ad_list=ads)

@admin_bp.route('/publicites/nouvelle', methods=['GET', 'POST'])
@login_required
@admin_required
def nouvelle_publicite():
    """Création d'une nouvelle publicité avec upload image"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('Le titre est obligatoire.', 'danger')
            return redirect(url_for('admin.nouvelle_publicite'))

        # Upload image publicité
        image_url = ''
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                url = save_upload(file, folder_key='ads', prefix='pub')
                if url:
                    image_url = url
                else:
                    flash('Format image non supporté. Utilisez JPG, PNG, WebP.', 'warning')

        ad = Advertisement(
            title      = title,
            image_url  = image_url,
            link_url   = request.form.get('link_url', '').strip(),
            content    = request.form.get('content', '').strip(),
            position   = request.form.get('position', 'banner_top'),
            is_active  = request.form.get('is_active') == 'on',
            sort_order = int(request.form.get('sort_order', 0) or 0),
        )
        db.session.add(ad)
        db.session.commit()
        flash(f'Publicité "{title}" créée avec succès !', 'success')
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

# ── GESTION DES ACTUALITÉS ───────────────────────────────────
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
    """Création d'un nouvel article avec image"""
    if request.method == 'POST':
        title_fr = request.form.get('title_fr', '').strip()
        if not title_fr:
            flash('Le titre est obligatoire.', 'danger')
            return redirect(url_for('admin.nouvel_article'))

        # Upload image article
        image_url = ''
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                url = save_upload(file, folder_key='articles', prefix='article')
                if url:
                    image_url = url

        from app.utils.helpers import slugify
        base_slug = slugify(title_fr)
        final_slug = base_slug
        counter = 1
        while Article.query.filter_by(slug=final_slug).first():
            final_slug = f"{base_slug}-{counter}"
            counter += 1

        article = Article(
            title_fr     = title_fr,
            title_ar     = request.form.get('title_ar', '').strip(),
            content_fr   = request.form.get('content_fr', ''),
            content_ar   = request.form.get('content_ar', ''),
            excerpt_fr   = request.form.get('excerpt_fr', '').strip(),
            image_url    = image_url,
            category     = request.form.get('category', 'annonce'),
            is_pinned    = request.form.get('is_pinned') == 'on',
            slug         = final_slug,
        )
        if request.form.get('publish_now') == 'on':
            article.publish()

        db.session.add(article)
        db.session.commit()
        flash('Article créé avec succès !', 'success')
        return redirect(url_for('admin.actualites'))

    return render_template('admin/article_form.html', article=None)

@admin_bp.route('/actualites/<int:id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_article(id):
    """Bascule la publication d'un article"""
    article = Article.query.get_or_404(id)
    if article.is_published:
        article.is_published = False
        article.published_at = None
        flash('Article dépublié.', 'warning')
    else:
        article.publish()
        flash('Article publié avec succès !', 'success')
    db.session.commit()
    return redirect(url_for('admin.actualites'))

@admin_bp.route('/actualites/<int:id>/supprimer', methods=['POST'])
@login_required
@admin_required
def supprimer_article(id):
    """Supprime définitivement un article"""
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash('Article supprimé.', 'success')
    return redirect(url_for('admin.actualites'))

# ── GESTION DE LA GALERIE ────────────────────────────────────
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
    """Ajoute une photo à la galerie"""
    if 'photo' not in request.files:
        flash('Aucun fichier sélectionné.', 'danger')
        return redirect(url_for('admin.galerie'))

    file = request.files['photo']
    if not file or not file.filename:
        flash('Fichier invalide.', 'danger')
        return redirect(url_for('admin.galerie'))

    url = save_upload(file, folder_key='gallery', prefix='galerie')
    if not url:
        flash('Format non supporté. Utilisez JPG, PNG, WebP.', 'danger')
        return redirect(url_for('admin.galerie'))

    photo = Gallery(
        image_url  = url,
        caption_fr = request.form.get('caption_fr', '').strip(),
        caption_ar = request.form.get('caption_ar', '').strip(),
        category   = request.form.get('category', 'activite'),
        sort_order = int(request.form.get('sort_order', 0) or 0),
        is_active  = True,
    )
    db.session.add(photo)
    db.session.commit()
    flash('Photo ajoutée avec succès !', 'success')
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

@admin_bp.route('/galerie/<int:id>/supprimer', methods=['POST'])
@login_required
@admin_required
def supprimer_photo(id):
    """Supprime une photo de la galerie"""
    photo = Gallery.query.get_or_404(id)
    db.session.delete(photo)
    db.session.commit()
    flash('Photo supprimée.', 'success')
    return redirect(url_for('admin.galerie'))

# ── PARAMÈTRES / LOGO ────────────────────────────────────────
@admin_bp.route('/parametres', methods=['GET', 'POST'])
@login_required
@admin_required
def parametres():
    """Paramètres du site — upload logo"""
    if request.method == 'POST':
        # Upload logo
        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename:
                url = save_logo(file)
                if url:
                    flash('Logo mis à jour avec succès ! Actualisez la page pour le voir.', 'success')
                else:
                    flash('Erreur upload logo. Utilisez JPG, PNG, SVG (max 32MB).', 'danger')
            else:
                flash('Aucun fichier sélectionné.', 'warning')
        return redirect(url_for('admin.parametres'))

    return render_template('admin/parametres.html')

# ── GESTION DES UTILISATEURS ────────────────────────────────
@admin_bp.route('/utilisateurs')
@login_required
@admin_required
def utilisateurs():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/utilisateurs.html', users=users)

@admin_bp.route('/utilisateurs/<int:id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_user(id):
    """Active ou désactive un compte utilisateur"""
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('Vous ne pouvez pas désactiver votre propre compte.', 'danger')
        return redirect(url_for('admin.utilisateurs'))
    user.is_active = not user.is_active
    db.session.commit()
    status = 'activé' if user.is_active else 'désactivé'
    flash(f'Compte {status} avec succès.', 'success')
    return redirect(url_for('admin.utilisateurs'))

@admin_bp.route('/utilisateurs/creer', methods=['POST'])
@login_required
@admin_required
def creer_utilisateur():
    """Crée un nouveau compte utilisateur"""
    full_name = request.form.get('full_name', '').strip()
    email     = request.form.get('email', '').strip().lower()
    password  = request.form.get('password', '').strip()
    role      = request.form.get('role', 'parent')

    if not all([full_name, email, password]):
        flash('Tous les champs obligatoires doivent être remplis.', 'danger')
        return redirect(url_for('admin.utilisateurs'))

    if User.query.filter_by(email=email).first():
        flash('Un compte avec cet email existe déjà.', 'danger')
        return redirect(url_for('admin.utilisateurs'))

    user = User(
        email=email, full_name=full_name,
        role=role, is_active=True,
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    flash(f'Compte créé pour {full_name} ({role}).', 'success')
    return redirect(url_for('admin.utilisateurs'))

# ── GESTION DES ÉVÉNEMENTS ──────────────────────────────────
@admin_bp.route('/evenements')
@login_required
@admin_required
def evenements():
    """Liste des événements du centre"""
    events = Event.query.order_by(Event.start_date.desc()).all()
    return render_template('admin/evenements.html', events=events)

# ── GESTION DES PAIEMENTS ───────────────────────────────────
@admin_bp.route('/paiements')
@login_required
@admin_required
def paiements():
    """Gestion des paiements"""
    payments = Payment.query.order_by(Payment.payment_date.desc()).all()
    return render_template('admin/paiements.html', payments=payments)

# ══════════════════════════════════════════════════════════════
# ROUTES CMS — Configuration complète du site
# L'admin modifie tout sans toucher au code Python
# ══════════════════════════════════════════════════════════════

@admin_bp.route('/configuration')
@login_required
@admin_required
def configuration():
    """Page principale de configuration du site"""
    categories = {
        'identite':     ('🏫', 'Identité du centre',    SiteSettings.get_all_by_category('identite')),
        'contact':      ('📞', 'Contact & Localisation', SiteSettings.get_all_by_category('contact')),
        'scolaire':     ('📅', 'Année scolaire',         SiteSettings.get_all_by_category('scolaire')),
        'statistiques': ('📊', 'Statistiques du site',  SiteSettings.get_all_by_category('statistiques')),
        'apparence':    ('🎨', 'Apparence',              SiteSettings.get_all_by_category('apparence')),
        'seo':          ('🔍', 'SEO & Référencement',    SiteSettings.get_all_by_category('seo')),
    }
    return render_template('admin/configuration.html', categories=categories)


@admin_bp.route('/configuration/sauvegarder', methods=['POST'])
@login_required
@admin_required
def sauvegarder_configuration():
    """Sauvegarde tous les paramètres du formulaire"""
    saved  = 0
    errors = 0

    for key, value in request.form.items():
        if key == 'csrf_token':
            continue
        try:
            SiteSettings.set(key, value.strip())
            saved += 1
        except Exception as e:
            errors += 1
            print(f"[CONFIG ERROR] {key}: {e}")

    if errors == 0:
        flash(f'✅ {saved} paramètre(s) mis à jour avec succès !', 'success')
    else:
        flash(f'⚠️ {saved} sauvegardés, {errors} erreur(s).', 'warning')

    return redirect(url_for('admin.configuration'))


@admin_bp.route('/configuration/statistiques', methods=['POST'])
@login_required
@admin_required
def sauvegarder_statistiques():
    """Sauvegarde rapide des statistiques"""
    stats_keys = ['stat_eleves', 'stat_enseignants', 'stat_reussite', 'stat_experience']
    for key in stats_keys:
        value = request.form.get(key, '').strip()
        if value:
            SiteSettings.set(key, value)
    flash('✅ Statistiques mises à jour !', 'success')
    return redirect(url_for('admin.configuration') + '#statistiques')


@admin_bp.route('/configuration/reset', methods=['POST'])
@login_required
@admin_required
def reset_configuration():
    """Remet une clé à sa valeur par défaut"""
    key = request.form.get('key', '')
    if key:
        SiteSettings.set(key, request.form.get('default_value', ''))
        flash(f'✅ Paramètre {key} réinitialisé.', 'info')
    return redirect(url_for('admin.configuration'))