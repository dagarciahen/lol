from flask import Blueprint, current_app, render_template, request, session, redirect, url_for
from flask_login import current_user
from itsdangerous import URLSafeTimedSerializer
from itsdangerous import BadSignature

from db import db
from ciceropage.forms.users import SignUpForm, SignUpCompletionForm
from ciceropage.models import User, Profile, Country, City

signup = Blueprint('signup', __name__, url_prefix='/sign-up')


@signup.route('', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = SignUpForm()
    sent_token = False
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get('email', None)
        if email:
            secret_key = current_app.config['SECRET_KEY']
            ts = URLSafeTimedSerializer(secret_key, salt='sign-up')
            verification_token = ts.dumps(email)
            print(verification_token)
            # TODO send email with activation link
            sent_token = verification_token is not None
    return render_template('pages/sign_up/sign-up.html', form=form, sent=sent_token)


@signup.route('/verify/<verification_token>', methods=['GET'])
def verify(verification_token):
    if verification_token:
        secret_key = current_app.config['SECRET_KEY']
        ts = URLSafeTimedSerializer(secret_key, salt='sign-up')
        try:
            email = ts.loads(verification_token, max_age=7200)  # 2 hours

            # set in a cookie the email for tyhe new account
            session['signup_email'] = email
        except BadSignature:
            print("Not a valid token.")
            email = None
    return render_template('pages/sign_up/verify.html', email=email)


@signup.route('/complete', methods=['GET', 'POST'])
def complete():
    form = SignUpCompletionForm()
    email = session.get('signup_email', None)
    created = False
    if email:
        # populate country list
        countries = Country.query.all()
        form.country.choices = [(country.country_id, country.name) for country in countries] if countries else [
            ('0', 'Select')
        ]
        if form.validate_on_submit():
            password = request.form.get('password')
            user = User(email, password)

            # add profile info
            profile = Profile()
            profile.name = request.form.get('name')
            profile.last_name = request.form.get('last_name')
            profile.bio = request.form.get('bio')
            profile.identification_type = request.form.get('identification_type')
            profile.identification_number = request.form.get('identification_number')
            profile.phone = request.form.get('phone')

            # add city to profile
            city = City.query.get(request.form.get('city'))
            profile.city_id = city.city_id

            user.profile = profile
            user.is_active = True

            db.session.add(user)
            db.session.commit()

            # eliminate tmp variable from session
            session.pop('signup_email')
            created = True
        return render_template('pages/sign_up/complete.html', form=form, created=created)
    return redirect(url_for('home.index'))
