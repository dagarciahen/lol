from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from ciceropage import db
from ciceropage.models import TourPost
from ciceropage.tour_posts.forms import TourPostForm

tour_posts = Blueprint('tour_posts',__name__)

@tour_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = TourPostForm()

    if form.validate_on_submit():

        tour_post = TourPost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id
                             )
        db.session.add(tour_post)
        db.session.commit()
        flash("Tour Post Created")
        return redirect(url_for('core.index'))

    return render_template('create_post.html',form=form)


# int: makes sure that the tour_post_id gets passed as in integer

@tour_posts.route('/<int:tour_post_id>')
def tour_post(tour_post_id):
    # grab the requested tour post by id number or return 404
    tour_post = TourPost.query.get_or_404(tour_post_id)
    return render_template('tour_post.html',title=tour_post.title,
                            date=tour_post.date,post=tour_post
    )

@tour_posts.route("/<int:tour_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(tour_post_id):
    tour_post = TourPost.query.get_or_404(tour_post_id)
    if tour_post.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = TourPostForm()
    if form.validate_on_submit():
        tour_post.title = form.title.data
        tour_post.text = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('tour_posts.tour_post', tour_post_id=tour_post.id))
    # Pass back the old tour post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = tour_post.title
        form.text.data = tour_post.text
    return render_template('create_post.html', title='Update',
                           form=form)


@tour_posts.route("/<int:tour_post_id>/delete", methods=['POST'])
@login_required
def delete_post(tour_post_id):
    tour_post = TourPost.query.get_or_404(tour_post_id)
    if tour_post.author != current_user:
        abort(403)
    db.session.delete(tour_post)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))
