from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils.decorators import parent_required
from app.models.student import Student
from app.models.attendance import Attendance
from app.models.payment import Payment

parent_bp = Blueprint('parent', __name__)

@parent_bp.route('/')
@login_required
@parent_required
def dashboard():
    parent   = current_user.parent_profile
    students = parent.students if parent else []
    return render_template('parent/dashboard.html',
                           parent=parent,
                           students=students)

@parent_bp.route('/presence/<int:student_id>')
@login_required
@parent_required
def presence(student_id):
    student    = Student.query.get_or_404(student_id)
    attendances = Attendance.query.filter_by(student_id=student_id).order_by(Attendance.date.desc()).limit(30).all()
    return render_template('parent/presence.html',
                           student=student,
                           attendances=attendances)

@parent_bp.route('/paiements/<int:student_id>')
@login_required
@parent_required
def paiements(student_id):
    student  = Student.query.get_or_404(student_id)
    payments = Payment.query.filter_by(student_id=student_id).order_by(Payment.payment_date.desc()).all()
    return render_template('parent/paiements.html',
                           student=student,
                           payments=payments)
