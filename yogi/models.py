from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    bio = db.Column(db.Text, default='')
    location = db.Column(db.String(120), default='')
    profile_picture = db.Column(db.String(255), default='default.png')
    signature_image = db.Column(db.String(255), nullable=True)  # Instructor signature image
    rating = db.Column(db.Float, default=0.0)
    is_admin = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    skills_offered = db.relationship('Skill', foreign_keys='Skill.user_id', backref='owner', lazy='dynamic')
    exchange_sent = db.relationship('ExchangeRequest', foreign_keys='ExchangeRequest.sender_id', backref='sender', lazy='dynamic')
    exchange_received = db.relationship('ExchangeRequest', foreign_keys='ExchangeRequest.receiver_id', backref='receiver', lazy='dynamic')
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reviews_given = db.relationship('Review', foreign_keys='Review.reviewer_id', backref='reviewer', lazy='dynamic')
    reviews_received = db.relationship('Review', foreign_keys='Review.reviewed_id', backref='reviewed', lazy='dynamic')
    reports_made = db.relationship('Report', foreign_keys='Report.reporter_id', backref='reporter', lazy='dynamic')
    reports_received = db.relationship('Report', foreign_keys='Report.reported_id', backref='reported', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_rating(self):
        reviews = self.reviews_received.all()
        if not reviews:
            return 0
        return sum(r.rating for r in reviews) / len(reviews)
    
    def get_avatar_color_class(self):
        """Returns a color class based on the username for avatar display."""
        # Use first letter of username to determine color (a-h = colors 1-8)
        if self.username:
            first_char = self.username[0].lower()
            if 'a' <= first_char <= 'h':
                return f'avatar-color-{ord(first_char) - ord("a") + 1}'
            elif 'i' <= first_char <= 'p':
                return f'avatar-color-{(ord(first_char) - ord("i")) % 8 + 1}'
            else:
                return f'avatar-color-{ord(first_char) % 8 + 1}'
        return 'avatar-color-1'
    
    def update_rating(self):
        self.rating = self.get_rating()
    
    @property
    def skills_count(self):
        return self.skills_offered.count()
    
    @property
    def exchanges_count(self):
        return self.exchange_sent.filter_by(status='completed').count()
    
    def __repr__(self):
        return f'<User {self.username}>'


class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    skill_type = db.Column(db.String(10), nullable=False)  # 'offered' or 'wanted'
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookmarks = db.relationship('Bookmark', backref='skill', lazy='dynamic', cascade='all, delete-orphan')
    exchange_requests_sender = db.relationship('ExchangeRequest', foreign_keys='ExchangeRequest.sender_skill_id', backref='sender_skill', lazy='dynamic')
    exchange_requests_receiver = db.relationship('ExchangeRequest', foreign_keys='ExchangeRequest.receiver_skill_id', backref='receiver_skill', lazy='dynamic')
    
    def __repr__(self):
        return f'<Skill {self.title}>'


class ExchangeRequest(db.Model):
    __tablename__ = 'exchange_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    sender_skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    receiver_skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    status = db.Column(db.String(20), default='pending', index=True)  # pending, accepted, rejected, completed
    message = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ExchangeRequest {self.id}>'


class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    is_read = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Message {self.id}>'


class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    reviewed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.id}>'


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'skill_id', name='unique_bookmark'),)
    
    def __repr__(self):
        return f'<Bookmark {self.id}>'


class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    reported_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending', index=True)  # pending, reviewed, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Report {self.id}>'


class Certificate(db.Model):
    __tablename__ = 'certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    exchange_id = db.Column(db.Integer, db.ForeignKey('exchange_requests.id'), nullable=False, index=True)
    skill_name = db.Column(db.String(100), nullable=False)
    instructor_name = db.Column(db.String(80), nullable=False)
    instructor_signature = db.Column(db.String(255), nullable=True)  # Store instructor signature image path
    completion_date = db.Column(db.DateTime, nullable=False)
    certificate_number = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='certificates')
    
    def __repr__(self):
        return f'<Certificate {self.certificate_number}>'

