from app import db
from datetime import datetime, timezone

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id         = db.Column(db.Integer,  primary_key=True)
    student_id = db.Column(db.Integer,  db.ForeignKey('students.id'), nullable=False)
    date       = db.Column(db.Date,     nullable=False)
    status     = db.Column(db.String(20), default='present')
    notes      = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    student = db.relationship('Student')

    def __repr__(self):
        return f'<Attendance {self.student_id} {self.date} {self.status}>'
