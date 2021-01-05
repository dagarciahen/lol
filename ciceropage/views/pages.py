from flask import Blueprint, render_template

pages = Blueprint('pages', __name__, url_prefix='/p')


@pages.route('/about', methods=['GET'])
def about():
    return render_template('info.html')


@pages.route('/pricing', methods=['GET'])
def pricing():
    return "Pricing"
