from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils.decorators import student_required

student_bp = Blueprint('student', __name__)

@student_bp.route('/')
@login_required
@student_required
def dashboard():
    student = current_user.student_profile
    return render_template('student/dashboard.html', student=student)
