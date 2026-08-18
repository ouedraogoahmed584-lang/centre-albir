from app import db
from datetime import datetime, timezone


class Article(db.Model):
    """Actualités et annonces du Centre Al-Bir"""
    __tablename__ = 'articles'

    id             = db.Column(db.Integer,     primary_key=True)
    title_fr       = db.Column(db.String(300), nullable=False)
    title_ar       = db.Column(db.String(300), nullable=True)
    content_fr     = db.Column(db.Text,        nullable=False)
    content_ar     = db.Column(db.Text,        nullable=True)
    excerpt_fr     = db.Column(db.String(500), nullable=True)
    image_url      = db.Column(db.String(500), nullable=True)
    category       = db.Column(db.String(50),  default='annonce')
    slug           = db.Column(db.String(300), unique=True, nullable=False)
    is_published   = db.Column(db.Boolean,     default=False)
    is_pinned      = db.Column(db.Boolean,     default=False)
    published_at   = db.Column(db.DateTime,    nullable=True)
    created_at     = db.Column(db.DateTime,    default=lambda: datetime.now(timezone.utc))
    updated_at     = db.Column(db.DateTime,    default=lambda: datetime.now(timezone.utc),
                               onupdate=lambda: datetime.now(timezone.utc))

    def publish(self):
        self.is_published = True
        self.published_at = datetime.now(timezone.utc)

    def __repr__(self):
        return f'<Article {self.title_fr[:50]}>'
