# ══════════════════════════════════════════════════════════════
# routes/auth.py — Authentification Centre Al-Bir
# Connexion et déconnexion uniquement.
# Pas de changement de mot de passe utilisateur.
# ══════════════════════════════════════════════════════════════

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from datetime import datetime, timezone

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for('public.accueil'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=bool(remember))
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()

            next_page = request.args.get('next')
            flash(f'Bienvenue, {user.full_name} !', 'success')

            if user.is_admin:
                return redirect(next_page or url_for('admin.dashboard'))
            elif user.is_parent:
                return redirect(next_page or url_for('parent.dashboard'))
            elif user.is_student:
                return redirect(next_page or url_for('student.dashboard'))
            return redirect(next_page or url_for('public.accueil'))
        else:
            flash('Email ou mot de passe incorrect.', 'danger')

    return render_template('auth/connexion.html')


@auth_bp.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('public.accueil'))
