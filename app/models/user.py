from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone


class User(UserMixin, db.Model):
    """
    Utilisateurs du système.
    Rôles : admin | teacher | parent | student
    """
    __tablename__ = 'users'

    id            = db.Column(db.Integer,     primary_key=True)
    email         = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name     = db.Column(db.String(150), nullable=False)
    role          = db.Column(db.String(20),  nullable=False, default='parent')
    is_active     = db.Column(db.Boolean,     default=True)
    avatar_url    = db.Column(db.String(300), nullable=True)
    phone         = db.Column(db.String(30),  nullable=True)
    created_at    = db.Column(db.DateTime,    default=lambda: datetime.now(timezone.utc))
    last_login    = db.Column(db.DateTime,    nullable=True)

    # Relations
    student_profile = db.relationship('Student', back_populates='user',   uselist=False)
    parent_profile  = db.relationship('Parent',  back_populates='user',   uselist=False)
    teacher_profile = db.relationship('Teacher', back_populates='user',   uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        self.last_login = datetime.now(timezone.utc)
        db.session.commit()

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_teacher(self):
        return self.role == 'teacher'

    @property
    def is_parent(self):
        return self.role == 'parent'

    @property
    def is_student(self):
        return self.role == 'student'

    def __repr__(self):
        return f'<User {self.email} [{self.role}]>'


@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
