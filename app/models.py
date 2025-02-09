from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import UniqueConstraint


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    hashed_password = db.Column(db.String(128))
    posts = db.relationship('Posts', backref='author')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password, method='bcrypt')

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_id(self):
        return str(self.id)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.Column(db.Integer, default=0)


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'declined', etc.

    __table_args__ = (
        UniqueConstraint('user_id', 'friend_id', name='_user_friend_uc'),
    )

    def __repr__(self):
        return f'<Friends {self.user_id} - {self.friend_id} ({self.status})>'