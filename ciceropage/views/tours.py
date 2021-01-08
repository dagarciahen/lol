from flask import Blueprint, render_template, request, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_

from db import db
from ..forms.tours import TourForm, TourEditForm, ReviewForm
from ..models import User, Tour, Review, Favorite, Country
from ..utils.picture_handler import upload_picture

tours = Blueprint('tours', __name__, url_prefix='/tours')

ROWS_PER_PAGE = 6


@tours.route('', methods=['GET'])
def list_all():
    page = request.args.get('page', 1, type=int)
    tour_list = Tour.query.filter_by(status='published').order_by(
        Tour.date.desc()
    ).paginate(
        page=page, per_page=ROWS_PER_PAGE
    )
    return render_template('pages/tours/list.html', tours=tour_list)


@tours.route('/by/me', methods=['GET'])
@login_required
def my():
    page = request.args.get('page', 1, type=int)
    tour_list = Tour.query.filter_by(user_id=current_user.user_id).order_by(
        Tour.date.desc()
    ).paginate(
        page=page, per_page=ROWS_PER_PAGE
    )
    return render_template('pages/tours/by.html', user=current_user, tours=tour_list)


@tours.route('/by/<int:user_id>', methods=['GET'])
@login_required
def by(user_id):
    user = User.query.get(user_id)
    page = request.args.get('page', 1, type=int)
    tour_list = Tour.query.filter_by(user_id=user_id).order_by(
        Tour.date.desc()
    )

    if current_user.user_id != user_id:
        tour_list = tour_list.filter_by(status='published')
    tour_list = tour_list.paginate(
        page=page, per_page=ROWS_PER_PAGE
    )
    return render_template('pages/tours/by.html', user=user, tours=tour_list)


@tours.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if current_user.type == 'tourist':
        abort(403)
    form = TourForm()
    if form.validate_on_submit():
        tour = Tour()
        tour.title = request.form.get('title')
        tour.description = request.form.get('description')
        tour.status = request.form.get('status')

        # get user id
        tour.user_id = current_user.user_id

        # get current location
        tour.country_id = current_user.profile.country_id
        tour.city = current_user.profile.city

        # add thumbnail
        thumbnail_file = form.thumbnail.data
        thumbnail = upload_picture(thumbnail_file, current_user.user_id, (540, 460), 'tours')
        tour.thumbnail = thumbnail

        # upload and save pictures

        # commit changes to db
        db.session.add(tour)
        db.session.commit()
        flash("Your tour has been saved.", category='success')
        return redirect(url_for('tours.my'))
    return render_template('pages/tours/new.html', form=form)


@tours.route('/<int:tour_id>', methods=['GET'])
def show(tour_id):
    tour = Tour.query.get_or_404(tour_id)

    # check if the item is public
    if tour.status in ['hidden', 'draft'] and tour.user_id != current_user.user_id:
        abort(403)

    # this is the form to post a review
    form = ReviewForm()

    # get reviews
    reviews = Review.query.filter_by(tour_id=tour_id).all()
    return render_template('pages/tours/show.html', tour=tour, reviews=reviews, form=form)


@tours.route('/<int:tour_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    form = TourEditForm()
    if tour.user_id != current_user.user_id:
        abort(403)
    form.title.data = tour.title
    form.status.data = tour.status
    form.description.data = tour.description

    if form.validate_on_submit():
        tour.title = request.form.get('title')
        tour.status = request.form.get('status')
        tour.description = request.form.get('description')

        # check if we have another picture
        if form.thumbnail.data:
            # add thumbnail
            thumbnail_file = form.thumbnail.data
            thumbnail = upload_picture(thumbnail_file, current_user.user_id, (540, 460), 'tours')
            tour.thumbnail = thumbnail

        db.session.add(tour)
        db.session.commit()
        flash("Your changes have been saved.", category='success')
        return redirect(url_for('tours.my'))
    return render_template('pages/tours/edit.html', form=form, tour=tour)


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


@tours.route('/<int:tour_id>/favorite', methods=['POST'])
@login_required
def favorite(tour_id):
    favorited = Favorite()
    favorited.user_id = current_user.user_id
    favorited.tour_id = tour_id
    db.session.add(favorited)
    db.session.commit()
    flash("Added to favorites", category='success')
    return redirect(url_for('tours.show', tour_id=tour_id))


@tours.route('/<int:tour_id>/unfavorite', methods=['POST'])
@login_required
def unfavorite(tour_id):
    favorited = Favorite.query.filter_by(tour_id=tour_id,user_id=current_user.user_id).first()

    if favorited:
        db.session.delete(favorited)
        db.session.commit()
        flash("Removed from favorites", category='success')
    else:
        flash("Couldn't remove from favorites", category='error')
    return redirect(url_for('tours.show', tour_id=tour_id))


@tours.route('/<int:tour_id>/reviews', methods=['POST'])
@login_required
def add_review(tour_id):
    form = ReviewForm()
    tour = Tour.query.get(tour_id)
    if current_user.user_id != tour.user_id:
        if form.validate_on_submit():
            review = Review()
            review.tour_id = tour_id
            review.user_id = current_user.user_id
            review.rating = int(request.form.get('rating'))
            review.comment = request.form.get('comment')

            db.session.add(review)
            db.session.commit()

            flash("Review added.", category='success')
    else:
        flash("You can't review your own tour.", category='error')
    return redirect(url_for('tours.show', tour_id=tour_id))


@tours.route('/<int:tour_id>/reviews/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(tour_id, review_id):
    return "Edit review"


@tours.route('/<int:tour_id>/reviews/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(tour_id, review_id):
    return "Delete review"


@tours.route('/search', methods=['GET', 'POST'])
def search():
    page = request.args.get('page', 1, type=int)
    if request.method == 'GET':
        q = request.args.get('q')
    else:
        q = request.form.get('q', None)
    if q:
        is_search = True
        tour_list = Tour.query.join(Country).filter(or_(
            Tour.title.ilike('%{}%'.format(q)),
            Tour.city.ilike('%{}%'.format(q)),
            Tour.description.ilike('%{}%'.format(q)),
            Country.name.ilike('%{}%'.format(q))
        )).paginate(
            page=page, per_page=ROWS_PER_PAGE
        )
    else:
        is_search = False
        tour_list = Tour.query.filter_by(
            status='published'
        ).paginate(
            page=page, per_page=ROWS_PER_PAGE
        )
    return render_template('pages/tours/list.html', q=q, tours=tour_list, is_search=is_search)
