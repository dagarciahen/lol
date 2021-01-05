from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import current_user, login_required

from ..models import Tour, User

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/<user_id>/profile', methods=['GET'])
def profile(user_id):
    if user_id == 'me':
        user = current_user
    else:
        user = User.query.get(int(user_id))
    if user:
        tours = Tour.query.filter_by(user_id=user.user_id).limit(10).all()
        return render_template('pages/users/profile.html', user=user, tours=tours)
    abort(404)


@users.route('/<int:user_id>/chat', methods=['GET', 'POST'])
def chat_to(user_id):
    if user_id == current_user.user_id:
        return redirect(url_for('home.index'))
    user = User.query.get(user_id)
    return render_template('pages/users/chat.html', user=user)
