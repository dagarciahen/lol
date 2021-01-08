from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, abort, request, flash
from flask_login import current_user, login_required
from sqlalchemy import and_, or_, func
from sqlalchemy.orm.util import AliasedClass

from db import db
from chatsocket import socket_io
from ..forms.users import ProfileForm
from ..models import Tour, User, Message, Country, Language, UserLanguage
from ..utils.picture_handler import upload_picture


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
        )
        if not current_user.is_authenticated or current_user.user_id != user.user_id:
            tour_list = tour_list.filter_by(status='published')
        tour_list = tour_list.paginate(
            page=page, per_page=10
        )
        return render_template('pages/users/profile.html', user=user, tours=tour_list)
    abort(404)


@users.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    user = User.query.get_or_404(current_user.user_id)
    if current_user.user_id != user_id:
        abort(403)
    form = ProfileForm()
    form.name.data = user.profile.name
    form.last_name.data = user.profile.last_name
    form.bio.data = user.profile.bio
    form.identification_type.data = user.profile.identification_type
    form.identification_number.data = user.profile.identification_number
    form.phone.data = user.profile.phone

    # populate country list
    countries = Country.query.all()
    form.country.choices = [(country.country_id, country.name) for country in countries] if countries else [
        ('0', 'Select')
    ]
    form.country.data = str(user.profile.country_id)
    form.city.data = user.profile.city

    # populate languages list
    form.languages.choices = [(language.language_id, language.name) for language in Language.query.all()]
    user_languages = UserLanguage.query.filter_by(user_id=user.user_id)
    form.languages.data = [user_language.language_id for user_language in user_languages]

    if form.validate_on_submit():
        user.profile.name = request.form.get('name')
        user.profile.last_name = request.form.get('last_name')
        user.profile.bio = request.form.get('bio')
        user.profile.identification_type = request.form.get('identification_type')
        user.profile.identification_number = request.form.get('identification_number')
        user.profile.phone = request.form.get('phone')

        user.profile.country_id = request.form.get('country')
        user.profile.city = request.form.get('city')

        # check if we have a new picture
        if form.picture.data:
            # add thumbnail
            picture_file = form.picture.data
            picture = upload_picture(picture_file, current_user.user_id, folder='profiles')
            user.profile.picture = picture

        # check if we have a new language
        selected_languages = request.form.getlist('languages')
        user_languages_add = []

        print(user_languages)

        if len(selected_languages) > 0:
            user_languages.delete()

        for selected_language in selected_languages:
            user_language_add = UserLanguage()
            user_language_add.user_id = current_user.user_id
            user_language_add.language_id = selected_language
            user_languages_add.append(user_language_add)

        # add languages
        db.session.bulk_save_objects(user_languages_add)

        db.session.add(user)
        db.session.commit()
        flash('Profile updated successfully.', category='success')
        return redirect(url_for('users.profile', user_id=user.user_id))
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
    ).order_by(Message.message_id.desc()).all()
    return render_template('pages/messages/all.html', messages=messages)
