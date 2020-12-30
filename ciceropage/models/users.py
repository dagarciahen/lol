from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from ciceropage import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(200))  # this is a hashed password
    is_active = db.Column(db.Boolean, default=False)
    joined_on = db.Column(db.DateTime, default=datetime.utcnow())

    profile = db.relationship('profile', uselist=False, back_populates="user")
    tours = db.relationship('tours')
    reviews = db.relationship('reviews')
    languages = db.relationship('users_languages')
    favorites = db.relationship('favorites')

    def __init__(self, email, passwd):
        self.email = email
        self.password = generate_password_hash(passwd)

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
