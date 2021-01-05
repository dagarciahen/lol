from flask import Blueprint, jsonify

from ..models import City, Region

locations = Blueprint('locations', __name__, url_prefix='/ajax')


@locations.route('/countries/<int:country_id>/regions', methods=['GET'])
def get_regions(country_id):
    print(country_id)
    regions = Region.query.filter_by(country_id=country_id)
    results = [region.to_dict() for region in regions]

    return jsonify(regions=results)


@locations.route('/regions/<int:region_id>/cities', methods=['GET'])
def get_cities(region_id):
    cities = City.query.filter_by(region_id=region_id)
    results = [city.to_dict() for city in cities]
    return jsonify(cities=results)

