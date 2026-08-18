from app import db
from datetime import datetime, timezone

class Gallery(db.Model):
    __tablename__ = 'gallery'
    id          = db.Column(db.Integer,     primary_key=True)
    image_url   = db.Column(db.String(500), nullable=False)
    caption_fr  = db.Column(db.String(300), nullable=True)
    caption_ar  = db.Column(db.String(300), nullable=True)
    category    = db.Column(db.String(50),  default='activite')
    sort_order  = db.Column(db.Integer,     default=0)
    is_active   = db.Column(db.Boolean,     default=True)
    created_at  = db.Column(db.DateTime,    default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Gallery {self.caption_fr}>'
