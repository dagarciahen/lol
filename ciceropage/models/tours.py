from datetime import datetime

from db import db
from . import User, Country


class Tour(db.Model):
    __tablename__ = 'tours'

    tour_id = db.Column(db.Integer, primary_key=True)
    thumbnail = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(140), nullable=False)
    city = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    # foreign keys
    country_id = db.Column(db.Integer, db.ForeignKey(Country.country_id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))

    images = db.relationship('Image')
    author = db.relationship('User')
    favorited_by = db.relationship('Favorite')

    country = db.relationship(Country)


class Image(db.Model):
    __tablename__ = 'images'

    image_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    tour_id = db.Column(db.Integer, db.ForeignKey(Tour.tour_id))


class Favorite(db.Model):
    __tablename__ = 'favorites'

    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey(Tour.tour_id), primary_key=True)

    favorites = db.relationship(User, back_populates="favorites")
    favorited_by = db.relationship(Tour, back_populates="favorited_by")
