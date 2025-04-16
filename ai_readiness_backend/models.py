from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData, UniqueConstraint, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from extensions import db, bcrypt

from flask_bcrypt import generate_password_hash, check_password_hash



metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db.metadata.naming_convention = metadata.naming_convention





# ----------------- User ------------------
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'admin', 'user'

    assessments = db.relationship('Assessment', backref='user', lazy=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    role = db.Column(db.String(50), default="user")

    # Use a property for password handling
    @property
    def password(self):
        raise AttributeError('Password is write-only.')

    @password.setter
    def password(self, raw_password):
        self.password_hash = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password_hash.encode('utf-8'))

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, "Invalid email address"
        return email

    @validates('role')
    def validate_role(self, key, role):
        assert role in ['user', 'admin'], "Invalid role"
        return role



# --------------- Organization ------------
class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100))
    size = db.Column(db.String(50))
    users = db.relationship("User", backref="organization", lazy=True)


# --------------- Assessment --------------
class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    overall_score = db.Column(db.Float)
    recommendation = db.Column(db.Text)

    use_case = db.relationship('UseCaseEvaluation', uselist=False, backref='assessment')
    data_readiness = db.relationship('DataReadinessEvaluation', uselist=False, backref='assessment')
    tech_infra = db.relationship('TechInfraEvaluation', uselist=False, backref='assessment')
    team_readiness = db.relationship('TeamReadinessEvaluation', uselist=False, backref='assessment')


# ------------- Use Case Evaluation -------------
class UseCaseEvaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))
    description = db.Column(db.Text)
    value = db.Column(db.Integer)         # 1–5
    feasibility = db.Column(db.Integer)   # 1–5
    priority = db.Column(db.Integer)      # 1–5


# ---------- Data Readiness Evaluation ----------
class DataReadinessEvaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))
    data_availability = db.Column(db.Integer)    # 1–5
    data_quality = db.Column(db.Integer)         # 1–5
    integration_level = db.Column(db.Integer)    # 1–5


# -------- Tech Infrastructure Evaluation --------
class TechInfraEvaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))
    cloud_ready = db.Column(db.Boolean)
    compute_power_score = db.Column(db.Integer)     # 1–5
    tools_stack_maturity = db.Column(db.Integer)    # 1–5
    apis_ready = db.Column(db.Boolean)


# -------- Team Readiness Evaluation --------
class TeamReadinessEvaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))
    ai_skills_level = db.Column(db.Integer)     # 1–5
    training_needs = db.Column(db.Text)
    leadership_support = db.Column(db.Integer)  # 1–5