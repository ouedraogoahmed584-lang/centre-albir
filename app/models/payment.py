from app import db
from datetime import datetime, timezone

class Payment(db.Model):
    __tablename__ = 'payments'
    id             = db.Column(db.Integer,     primary_key=True)
    student_id     = db.Column(db.Integer,     db.ForeignKey('students.id'), nullable=False)
    amount_fcfa    = db.Column(db.Integer,     nullable=False)
    payment_date   = db.Column(db.Date,        nullable=False)
    school_year    = db.Column(db.String(20),  default='2026/2027')
    payment_method = db.Column(db.String(50),  default='especes')
    receipt_number = db.Column(db.String(50),  nullable=True)
    notes          = db.Column(db.Text,        nullable=True)
    created_at     = db.Column(db.DateTime,    default=lambda: datetime.now(timezone.utc))

    student = db.relationship('Student')

    def __repr__(self):
        return f'<Payment {self.amount_fcfa} FCFA - {self.student_id}>'
