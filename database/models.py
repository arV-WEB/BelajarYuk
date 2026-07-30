from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database.connection import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    field_of_study = db.Column(db.String(128), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_pic = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    settings = db.relationship('Settings', backref='user', uselist=False, cascade="all, delete-orphan")
    events = db.relationship('Event', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    goals = db.relationship('Goal', backref='user', lazy='dynamic', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Settings(db.Model):
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    email_notifications = db.Column(db.Boolean, default=True)
    study_reminders = db.Column(db.Boolean, default=True)
    weekly_summary = db.Column(db.Boolean, default=True)
    goal_alerts = db.Column(db.Boolean, default=True)
    theme = db.Column(db.String(10), default='light')
    language = db.Column(db.String(20), default='en-US')
    timezone = db.Column(db.String(50), default='Mountain Time (MT)')

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(50), default='Study Sessions')  # Study Sessions, Deadlines, Exams, Reminders
    all_day = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description or '',
            'start': self.start_time.isoformat(),
            'end': self.end_time.isoformat(),
            'category': self.category,
            'allDay': self.all_day
        }

class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(50), default='Academic')  # Academic, Personal, Career, Skill
    description = db.Column(db.Text, nullable=True)
    target_date = db.Column(db.Date, nullable=True)
    progress = db.Column(db.Integer, default=0)  # 0 - 100
    status = db.Column(db.String(20), default='In Progress')  # In Progress, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'description': self.description or '',
            'targetDate': self.target_date.isoformat() if self.target_date else None,
            'progress': self.progress,
            'status': self.status
        }
