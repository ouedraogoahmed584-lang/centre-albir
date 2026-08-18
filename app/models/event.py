from app import db
from datetime import datetime, timezone

class Event(db.Model):
    __tablename__ = 'events'
    id             = db.Column(db.Integer,     primary_key=True)
    title_fr       = db.Column(db.String(300), nullable=False)
    title_ar       = db.Column(db.String(300), nullable=True)
    description_fr = db.Column(db.Text,        nullable=True)
    start_date     = db.Column(db.DateTime,    nullable=False)
    end_date       = db.Column(db.DateTime,    nullable=True)
    location       = db.Column(db.String(200), nullable=True)
    is_public      = db.Column(db.Boolean,     default=True)
    category       = db.Column(db.String(50),  default='general')
    created_at     = db.Column(db.DateTime,    default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Event {self.title_fr[:50]}>'
