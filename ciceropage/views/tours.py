from flask import Blueprint, render_template, request, abort, flash
from flask_login import login_required, current_user

from db import db
from ..forms.tours import TourForm
from ..models import User, Tour, Image
from ..utils.picture_handler import upload_picture

tours = Blueprint('tours', __name__, url_prefix='/tours')


@tours.route('', methods=['GET'])
def list_all():
    tour_list = Tour.query.filter_by(status='published')
    return render_template('pages/tours/list.html', tours=tour_list)


@tours.route('/by/me', methods=['GET'])
def my():
    tour_list = Tour.query.filter_by(user_id=current_user.user_id)
    for tour in tour_list:
        print(tour)
    return render_template('pages/tours/by_me.html', tours=tour_list)


@tours.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = TourForm()
    if form.validate_on_submit():
        print('valid')
        tour = Tour()
        tour.title = request.form.get('title')
        tour.description = request.form.get('description')
        tour.status = request.form.get('status')

        # get user id
        tour.user_id = current_user.user_id

        # get current city
        tour.city_id = current_user.profile.city_id

        # add thumbnail
        thumbnail_file = form.thumbnail.data
        thumbnail = upload_picture(thumbnail_file, current_user.user_id, (540, 460), 'tours')
        tour.thumbnail = thumbnail

        # upload and save pictures


        # commit changes to db
        db.session.add(tour)
        db.session.commit()
        flash("Your tour has been saved.")
    return render_template('pages/tours/new.html', form=form)


@tours.route('/<int:tour_id>', methods=['GET'])
def show(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    return render_template('pages/tours/show.html', tour=tour)


@tours.route('/<int:tour_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(tour_id):
    form = TourForm()
    tour = Tour.query.get_or_404(tour_id)
    if tour.user_id != current_user.user_id:
        abort(403)
    form.title = tour.title
    form.status = tour.status
    form.description = tour.description
    if form.validate_on_submit():
        print('modify form')
    return render_template('pages/tours/edit.html', form=form)


@tours.route('/<int:tour_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(tour_id):
    # TODO add form
    tour = Tour.query.get_or_404()
    if tour.user_id != current_user.user_id:
        abort(410)
    db.session.delete(tour)
    db.session.commit()
    return "Delete tour: {}".format(tour_id)


@tours.route('/<int:tour_id>/reviews', methods=['POST'])
@login_required
def add_review(tour_id):
    return "Add review"


@tours.route('/<int:tour_id>/reviews/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(tour_id, review_id):
    return "Edit review"


@tours.route('/<int:tour_id>/reviews/<int:review_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_review(tour_id, review_id):
    return "Delete review"
