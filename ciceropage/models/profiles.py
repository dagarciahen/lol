from db import db
from . import User, Country


class Profile(db.Model):
    __tablename__ = 'profiles'

    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    picture = db.Column(db.Text)
    city = db.Column(db.Text)
    name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    bio = db.Column(db.Text)
    identification_type = db.Column(db.String(10), nullable=False)
    identification_number = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(14))

    country_id = db.Column(db.Integer, db.ForeignKey(Country.country_id))

    user = db.relationship(User, back_populates="profile")
    country = db.relationship(Country)
