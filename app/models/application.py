from app import db
from datetime import datetime, timezone


class Application(db.Model):
    """
    Demandes d'inscription au Centre Al-Bir.
    Pipeline : pending → docs_received → under_review → accepted/rejected → enrolled
    """
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)

    # Référence unique
    reference = db.Column(db.String(20), unique=True, nullable=False)

    # Informations parent/tuteur
    parent_name     = db.Column(db.String(150), nullable=False)
    parent_phone    = db.Column(db.String(30),  nullable=False)
    parent_whatsapp = db.Column(db.String(30),  nullable=True)
    parent_email    = db.Column(db.String(150), nullable=True)

    # Informations élève
    student_name  = db.Column(db.String(150), nullable=False)
    student_age   = db.Column(db.Integer,     nullable=False)
    student_level = db.Column(db.String(100), nullable=True)
    motivation    = db.Column(db.Text,        nullable=True)

    # Programme souhaité
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=True)
    program    = db.relationship('Program', back_populates='applications')

    # Documents uploadés
    doc_bulletin_url    = db.Column(db.String(500), nullable=True)
    doc_certificate_url = db.Column(db.String(500), nullable=True)
    doc_photo_url       = db.Column(db.String(500), nullable=True)

    # Statut du dossier
    status       = db.Column(db.String(50), default='pending')
    admin_notes  = db.Column(db.Text,       nullable=True)

    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at   = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                             onupdate=lambda: datetime.now(timezone.utc))

    STATUS_LABELS = {
        'pending':        'En attente',
        'docs_received':  'Documents reçus',
        'under_review':   'En cours d\'examen',
        'accepted':       'Accepté',
        'rejected':       'Refusé',
        'enrolled':       'Inscrit',
    }

    STATUS_COLORS = {
        'pending':        'gray',
        'docs_received':  'blue',
        'under_review':   'yellow',
        'accepted':       'green',
        'rejected':       'red',
        'enrolled':       'emerald',
    }

    @property
    def status_label(self):
        return self.STATUS_LABELS.get(self.status, self.status)

    @property
    def status_color(self):
        return self.STATUS_COLORS.get(self.status, 'gray')

    def generate_reference(self):
        import random, string
        chars = string.ascii_uppercase + string.digits
        self.reference = 'ALB-' + ''.join(random.choices(chars, k=8))

    def __repr__(self):
        return f'<Application {self.reference} - {self.student_name}>'
