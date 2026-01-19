"""
Database Models for Face Attendance System
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    """Teacher/User model for login"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='teacher', nullable=False)  # admin, teacher, student
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    attendance_records = db.relationship('Attendance', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    def check_password(self, password):
        """Verify password"""
        try:
            return bcrypt.checkpw(password.encode(), self.password_hash.encode())
        except:
            return False
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def is_teacher(self):
        """Check if user is teacher or admin"""
        return self.role in ['admin', 'teacher']
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }


class Attendance(db.Model):
    """Attendance record model"""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    time = db.Column(db.Time, nullable=False)
    confidence = db.Column(db.Float, default=0.0)  # Face recognition confidence score
    photo_path = db.Column(db.String(255))  # Path to captured photo
    marked_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Which teacher marked it
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Composite unique constraint: one person per day
    __table_args__ = (
        db.UniqueConstraint('name', 'date', name='unique_attendance_per_day'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.isoformat(),
            'time': self.time.isoformat(),
            'confidence': round(self.confidence, 2),
            'photo_path': self.photo_path,
            'created_at': self.created_at.isoformat()
        }


class Dataset(db.Model):
    """Face dataset metadata"""
    __tablename__ = 'datasets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    image_count = db.Column(db.Integer, default=0)
    encoding_hash = db.Column(db.String(255))  # Hash of current encodings
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'name': self.name,
            'image_count': self.image_count,
            'last_updated': self.last_updated.isoformat()
        }
