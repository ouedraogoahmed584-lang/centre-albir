from app import db
from datetime import datetime, timezone


class Program(db.Model):
    """
    Programmes enseignés au Centre Al-Bir.
    Gérés entièrement par l'administrateur.
    """
    __tablename__ = 'programs'

    id             = db.Column(db.Integer,     primary_key=True)
    name_fr        = db.Column(db.String(150), nullable=False)
    name_ar        = db.Column(db.String(150), nullable=True)
    description_fr = db.Column(db.Text,        nullable=True)
    description_ar = db.Column(db.Text,        nullable=True)
    objectives_fr  = db.Column(db.Text,        nullable=True)
    department     = db.Column(db.String(50),  nullable=False, default='islamic')
    language       = db.Column(db.String(50),  nullable=True)
    min_age        = db.Column(db.Integer,     default=15)
    max_age        = db.Column(db.Integer,     default=50)
    duration       = db.Column(db.String(100), nullable=True)
    icon           = db.Column(db.String(10),  default='📖')
    color          = db.Column(db.String(20),  default='#064E3B')
    slug           = db.Column(db.String(150), unique=True, nullable=False)
    sort_order     = db.Column(db.Integer,     default=0)
    is_active      = db.Column(db.Boolean,     default=True)
    created_at     = db.Column(db.DateTime,    default=lambda: datetime.now(timezone.utc))

    # Relation
    applications = db.relationship('Application', back_populates='program')

    def __repr__(self):
        return f'<Program {self.name_fr}>'
