from flask import render_template,request,Blueprint
from ciceropage.models import TourPost

core = Blueprint('core',__name__)

@core.route('/')
def index():

    page = request.args.get('page', 1, type=int)
    tour_posts = TourPost.query.order_by(TourPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html',tour_posts=tour_posts)

@core.route('/info')
def info():

    return render_template('info.html')
