from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """Décorateur : accès réservé aux administrateurs"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.connexion'))
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def parent_required(f):
    """Décorateur : accès réservé aux parents"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.connexion'))
        if current_user.role not in ['parent', 'admin']:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def student_required(f):
    """Décorateur : accès réservé aux élèves"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.connexion'))
        if current_user.role not in ['student', 'admin']:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
