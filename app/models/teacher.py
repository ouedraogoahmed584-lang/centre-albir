from app import db
from datetime import datetime, timezone

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id            = db.Column(db.Integer,     primary_key=True)
    user_id       = db.Column(db.Integer,     db.ForeignKey('users.id'), unique=True)
    full_name     = db.Column(db.String(150), nullable=False)
    speciality    = db.Column(db.String(200), nullable=True)
    qualification = db.Column(db.String(300), nullable=True)
    bio           = db.Column(db.Text,        nullable=True)
    photo_url     = db.Column(db.String(300), nullable=True)
    phone         = db.Column(db.String(30),  nullable=True)
    is_active     = db.Column(db.Boolean,     default=True)
    show_on_site  = db.Column(db.Boolean,     default=True)
    sort_order    = db.Column(db.Integer,     default=0)
    created_at    = db.Column(db.DateTime,    default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='teacher_profile')

    def __repr__(self):
        return f'<Teacher {self.full_name}>'
