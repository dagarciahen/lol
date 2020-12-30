from ciceropage import db


class Country(db.Model):
    __tablename__ = 'countries'

    country_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    calling_code = db.Column(db.String(4), nullable=False)
    iso_code = db.Column(db.String(4), nullable=False)
    regions = db.relationship("Region")


class Region(db.Model):
    __tablename__ = 'regions'

    region_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    cities = db.relationship("City")

    country_id = db.Column(db.Integer, db.ForeignKey('countries.country_id'))


class City(db.Model):
    __tablename__ = 'cities'

    city_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    region_id = db.Column(db.Integer, db.ForeignKey('regions.region_id'))
