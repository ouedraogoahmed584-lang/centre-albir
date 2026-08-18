from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from datetime import datetime, timezone
# Ajouter l'import si manquant
from flask_login import login_required, login_user, logout_user, current_user
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



# ══════════════════════════════════════════════════════════════
# ROUTE — Changement de mot de passe sécurisé
# Vérifie le mot de passe actuel avant d'autoriser le changement
# ══════════════════════════════════════════════════════════════

@auth_bp.route('/changer-mot-de-passe', methods=['GET', 'POST'])
@login_required
def changer_mot_de_passe():
    """Page de changement de mot de passe pour tout utilisateur connecté"""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password     = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Vérification mot de passe actuel
        if not current_user.check_password(current_password):
            flash('Mot de passe actuel incorrect.', 'danger')
            return redirect(url_for('auth.changer_mot_de_passe'))

        # Vérification correspondance
        if new_password != confirm_password:
            flash('Les nouveaux mots de passe ne correspondent pas.', 'danger')
            return redirect(url_for('auth.changer_mot_de_passe'))

        # Vérification longueur minimale
        if len(new_password) < 8:
            flash('Le mot de passe doit contenir au moins 8 caractères.', 'danger')
            return redirect(url_for('auth.changer_mot_de_passe'))

        # Mise à jour
        current_user.set_password(new_password)
        db.session.commit()

        flash('Mot de passe modifié avec succès ! Reconnectez-vous.', 'success')
        logout_user()
        return redirect(url_for('auth.connexion'))

    return render_template('auth/changer_mot_de_passe.html')