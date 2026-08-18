from app import db
from datetime import datetime, timezone

class Parent(db.Model):
    __tablename__ = 'parents'
    id          = db.Column(db.Integer,     primary_key=True)
    user_id     = db.Column(db.Integer,     db.ForeignKey('users.id'), unique=True)
    full_name   = db.Column(db.String(150), nullable=False)
    phone       = db.Column(db.String(30),  nullable=True)
    whatsapp    = db.Column(db.String(30),  nullable=True)
    email       = db.Column(db.String(150), nullable=True)
    address     = db.Column(db.String(300), nullable=True)
    created_at  = db.Column(db.DateTime,    default=lambda: datetime.now(timezone.utc))

    user     = db.relationship('User',    back_populates='parent_profile')
    students = db.relationship('Student', back_populates='parent')

    def __repr__(self):
        return f'<Parent {self.full_name}>'
