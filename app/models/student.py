from app import db
from datetime import datetime, timezone

class Student(db.Model):
    __tablename__ = 'students'
    id            = db.Column(db.Integer,     primary_key=True)
    user_id       = db.Column(db.Integer,     db.ForeignKey('users.id'), unique=True)
    student_number= db.Column(db.String(20),  unique=True, nullable=True)
    full_name     = db.Column(db.String(150), nullable=False)
    birth_date    = db.Column(db.Date,        nullable=True)
    age           = db.Column(db.Integer,     nullable=True)
    program_id    = db.Column(db.Integer,     db.ForeignKey('programs.id'), nullable=True)
    enrollment_date = db.Column(db.Date,      nullable=True)
    school_year   = db.Column(db.String(20),  default='2026/2027')
    status        = db.Column(db.String(30),  default='active')
    photo_url     = db.Column(db.String(300), nullable=True)
    notes         = db.Column(db.Text,        nullable=True)
    created_at    = db.Column(db.DateTime,    default=lambda: datetime.now(timezone.utc))

    user    = db.relationship('User',    back_populates='student_profile')
    program = db.relationship('Program')
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=True)
    parent    = db.relationship('Parent', back_populates='students')

    def __repr__(self):
        return f'<Student {self.full_name}>'
