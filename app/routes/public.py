from flask import Blueprint, render_template, abort
from app.models.program import Program
from app.models.article import Article
from app.models.gallery import Gallery
from app.models.event import Event
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
