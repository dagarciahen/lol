from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from db import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(200))  # this is a hashed password
    type = db.Column(db.String(100), default='tourist')
    is_active = db.Column(db.Boolean, default=False)
    joined_on = db.Column(db.DateTime, default=datetime.utcnow())

    profile = db.relationship('Profile', uselist=False, back_populates="user")
    tours = db.relationship('Tour', back_populates="author")
    reviews = db.relationship('Review', back_populates="user")
    languages = db.relationship('UserLanguage')
    favorites = db.relationship('Favorite')

    def __init__(self, email, passwd):
        self.email = email
        self.password = generate_password_hash(passwd)

    def get_id(self):
        return self.user_id

    def get_hashed_id(self):
        return hash(self.email)

    def check_password(self, passwd):
        return check_password_hash(self.password, passwd)


class Language(db.Model):
    __tablename__ = 'languages'

    language_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4), nullable=False)
    name = db.Column(db.String(40), nullable=False)


class UserLanguage(db.Model):
    __tablename__ = 'users_languages'

    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey(Language.language_id), primary_key=True)

    user = db.relationship(User, back_populates="languages")
    language = db.relationship(Language)
