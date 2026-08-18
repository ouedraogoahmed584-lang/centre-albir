# ══════════════════════════════════════════════════════════════
# app/models/site_settings.py
# Table clé-valeur pour tous les paramètres du site
# L'admin modifie tout sans toucher au code
# ══════════════════════════════════════════════════════════════

from app import db
from datetime import datetime, timezone


class SiteSettings(db.Model):
    """
    Table de configuration dynamique du site Centre Al-Bir.
    Chaque paramètre = une ligne (clé, valeur, catégorie).
    L'administrateur modifie tout depuis le panneau admin.
    """
    __tablename__ = 'site_settings'

    id         = db.Column(db.Integer,     primary_key=True)
    key        = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value      = db.Column(db.Text,        nullable=True)
    label      = db.Column(db.String(200), nullable=True)  # Libellé affiché à l'admin
    category   = db.Column(db.String(50),  nullable=False, default='general')
    field_type = db.Column(db.String(20),  nullable=False, default='text')
    # Types : text | textarea | number | email | tel | url | image | boolean | color
    sort_order = db.Column(db.Integer,     default=0)
    updated_at = db.Column(db.DateTime,
                           default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<SiteSettings {self.key}={self.value[:30] if self.value else ""}>'

    @classmethod
    def get(cls, key, default=''):
        """Récupère une valeur par clé"""
        setting = cls.query.filter_by(key=key).first()
        return setting.value if setting and setting.value else default

    @classmethod
    def set(cls, key, value):
        """Définit une valeur"""
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            setting.updated_at = datetime.now(timezone.utc)
        else:
            setting = cls(key=key, value=value)
            db.session.add(setting)
        db.session.commit()

    @classmethod
    def get_all_by_category(cls, category):
        """Retourne tous les paramètres d'une catégorie"""
        return cls.query.filter_by(category=category).order_by(cls.sort_order).all()

    @classmethod
    def get_dict(cls):
        """Retourne tous les paramètres en dictionnaire {key: value}"""
        settings = cls.query.all()
        return {s.key: s.value or '' for s in settings}
