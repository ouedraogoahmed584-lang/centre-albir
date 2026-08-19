from app import db
from datetime import datetime, timezone


class Advertisement(db.Model):
    """
    Publicités/Annonces gérées entièrement par l'administrateur.
    Affichées sur le site public selon leur position et dates.
    """
    __tablename__ = 'advertisements'
    __table_args__ = (
        db.Index('ix_ads_active_pos', 'is_active', 'position'),
    )

    id         = db.Column(db.Integer,     primary_key=True)
    title      = db.Column(db.String(200), nullable=False)
    image_url  = db.Column(db.String(500), nullable=True)
    link_url   = db.Column(db.String(500), nullable=True)
    content    = db.Column(db.Text,        nullable=True)

    # Position sur le site
    position   = db.Column(db.String(50), nullable=False, default='banner_top')
    # Valeurs : hero | banner_top | banner_bottom | sidebar | between_sections

    is_active  = db.Column(db.Boolean,  default=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date   = db.Column(db.DateTime, nullable=True)
    sort_order = db.Column(db.Integer,  default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    @property
    def is_currently_active(self):
        now = datetime.now(timezone.utc)
        if not self.is_active:
            return False
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True

    def __repr__(self):
        return f'<Ad {self.title} [{self.position}]>'
