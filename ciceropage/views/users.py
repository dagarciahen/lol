from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask_login import current_user, login_required
from sqlalchemy import and_, or_, func
from sqlalchemy.orm.util import AliasedClass

from ..forms.users import ProfileForm
from ..models import Tour, User, Message
from chatsocket import socket_io

from db import db

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/<user_id>/profile', methods=['GET'])
def profile(user_id):
    if user_id == 'me':
        user = current_user
    else:
        user = User.query.get(int(user_id))
    if user:
        page = request.args.get('page', 1, type=int)
        tour_list = Tour.query.filter_by(user_id=user.user_id).order_by(
            Tour.date.desc()
        ).paginate(
            page=page, per_page=10
        )
        return render_template('pages/users/profile.html', user=user, tours=tour_list)
    abort(404)


@users.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    if current_user.user_id != user_id:
        abort(403)
    form = ProfileForm()
    user = User.query.get(current_user.user_id)

    form.name = user.profile.name
    form.last_name = user.profile.last_name
    form.bio = user.profile.bio
    form.identification_type = user.profile.identification_type
    form.identification_number = user.profile.identification_number
    form.phone = user.profile.phone

    if form.validate_on_submit():
        # TODO update info
        # update info
        pass
    return render_template('pages/users/edit.html', form=form)


@users.route('/me/message/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat_to(user_id):
    if user_id == current_user.user_id:
        return redirect(url_for('home.index'))
    user = User.query.get(user_id)

    # get messages
    messages = Message.query.filter(
        and_(
            Message.sender_id.in_((current_user.user_id, user.user_id)),
            Message.recipient_id.in_((current_user.user_id, user.user_id)))
    ).order_by(Message.message_id.asc()).all()

    return render_template('pages/messages/show.html', user=user, messages=messages)


@socket_io.on('online')
def handle_online(json):
    socket_io.emit('online', json)


@socket_io.on('chat')
def handle_message(data):
    msg = data.get('message')
    if msg != '':
        user = User.query.get(data.get('to'))
        message = Message()
        message.message = msg
        message.sender_id = current_user.user_id
        message.recipient_id = user.user_id
        message.date = datetime.utcnow()

        db.session.add(message)
        db.session.commit()

        message = Message.query.filter(
            and_(
                Message.sender_id.in_((current_user.user_id, user.user_id)),
                Message.recipient_id.in_((current_user.user_id, user.user_id)))
        ).order_by(Message.message_id.desc()).first()

        result = message.to_dict()

        emit_to = '{}@{}'.format(user.user_id, hash(current_user.email))
        emit_from = '{}@{}'.format(current_user.user_id, hash(user.email))
        socket_io.emit(emit_to, result)
        socket_io.emit(emit_from, result)


@users.route('/me/messages')
@login_required
def my_messages():
    m = AliasedClass(Message)

    messages = Message.query.filter(
        or_(Message.sender_id == current_user.user_id, Message.recipient_id == current_user.user_id),
        Message.date.in_(
            db.session.query(func.max(m.date)).filter(
                or_(
                    and_(Message.sender_id == m.sender_id, Message.recipient_id == m.recipient_id),
                    and_(Message.sender_id == m.recipient_id, Message.recipient_id == m.sender_id)
                )
            )
        )
    ).order_by(Message.message_id.desc())
    return render_template('pages/messages/all.html', messages=messages)
