from itsdangerous import URLSafeTimedSerializer
from itsdangerous import BadSignature
from flask import Blueprint, current_app, render_template, request, session, redirect, url_for
from flask_login import current_user
from flask_mail import Message

from db import db
from mail import mail
from ciceropage.forms.users import SignUpForm, SignUpCompletionForm
from ciceropage.models import User, Profile, Country

signup = Blueprint('signup', __name__, url_prefix='/sign-up')


@signup.route('', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = SignUpForm()
    sent_token = False
    user_type = request.args.get('account_type', 'tourist')
    if request.method == 'POST' and form.validate_on_submit():
        user_type = user_type if user_type in ['tourist', 'guide'] else 'tourist'
        email = request.form.get('email', None)
        if email:
            secret_key = current_app.config['SECRET_KEY']
            ts = URLSafeTimedSerializer(secret_key, salt='sign-up')
            verification_token = ts.dumps({"email": email, "user_type": user_type})
            url_token = '{}/sign-up/verify/{}'.format(current_app.config['SITE_URL'], verification_token)
            msg = Message("Verify account", sender=("Cicero demo", current_app.config['MAIL_USERNAME']))
            msg.recipients = [email]
            msg.body = 'Complete your account information'
            msg.html = render_template('mail.html', url_token=url_token)
            mail.send(msg)
            sent_token = verification_token is not None
    return render_template('pages/sign_up/sign-up.html', form=form, sent=sent_token, account_type=user_type)


@signup.route('/verify/<verification_token>', methods=['GET'])
def verify(verification_token):
    if verification_token:
        secret_key = current_app.config['SECRET_KEY']
        ts = URLSafeTimedSerializer(secret_key, salt='sign-up')
        try:
            data = ts.loads(verification_token, max_age=7200)  # 2 hours
            # set in a cookie the email for the new account
            session['signup_data'] = data
        except BadSignature:
            print("Not a valid token.")
            data = None
    return render_template('pages/sign_up/verify.html', data=data)


@signup.route('/complete', methods=['GET', 'POST'])
def complete():
    form = SignUpCompletionForm()
    data = session.get('signup_data', None)
    created = False
    if data:
        # populate country list
        countries = Country.query.all()
        form.country.choices = [(country.country_id, country.name) for country in countries] if countries else [
            ('0', 'Select')
        ]
        if form.validate_on_submit():
            password = request.form.get('password')
            user = User(data.get('email'), password)
            user.type = data.get('user_type')

            # add profile info
            profile = Profile()
            profile.name = request.form.get('name')
            profile.last_name = request.form.get('last_name')
            profile.bio = request.form.get('bio')
            profile.identification_type = request.form.get('identification_type')
            profile.identification_number = request.form.get('identification_number')
            profile.phone = request.form.get('phone')

            # add city to profile
            profile.city = request.form.get('city')
            profile.country_id = request.form.get('country')

            user.profile = profile
            user.is_active = True

            db.session.add(user)
            db.session.commit()

            # eliminate tmp variable from session
            session.pop('signup_data')
            created = True
        return render_template('pages/sign_up/complete.html', form=form, created=created)
    return redirect(url_for('home.index'))
