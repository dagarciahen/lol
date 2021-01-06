from db import db


class Country(db.Model):
    __tablename__ = 'countries'

    country_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    calling_code = db.Column(db.String(4), nullable=False)
    iso_code = db.Column(db.String(4), nullable=False)
    regions = db.relationship("Region")

    regions = db.relationship("Region", back_populates="country")


class Region(db.Model):
    __tablename__ = 'regions'

    region_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    cities = db.relationship("City")

    country_id = db.Column(db.Integer, db.ForeignKey('countries.country_id'))

    cities = db.relationship("City", back_populates="region")
    country = db.relationship("Country")

    def to_dict(self):
        return {
            "region_id": self.region_id,
            "name": self.name
        }


class City(db.Model):
    __tablename__ = 'cities'

    city_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    region_id = db.Column(db.Integer, db.ForeignKey('regions.region_id'))

    region = db.relationship("Region")
    tours = db.relationship("Tour", back_populates="location")

    def to_dict(self):
        return {
            "city_id": self.city_id,
            "name": self.name
        }
