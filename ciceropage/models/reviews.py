from datetime import datetime

from db import db
from . import User, Tour


class Review(db.Model):
    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    tour_id = db.Column(db.Integer, db.ForeignKey(Tour.tour_id))

    user = db.relationship("User")
