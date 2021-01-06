from db import db


class Country(db.Model):
    __tablename__ = 'countries'

    country_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    calling_code = db.Column(db.String(4), nullable=False)
    iso_code = db.Column(db.String(4), nullable=False)

    tours = db.relationship("Tour", back_populates="country")
    users = db.relationship("Profile", back_populates="country")

