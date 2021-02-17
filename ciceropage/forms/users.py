from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from ciceropage.models import User

IDENTIFICATION_TYPE_CHOICES = [
    ('id', 'ID'),
    ('passport', 'Passport'),
    ('driver license', 'Drivers license')
]


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('An account already exists for this email address. Please use another one.')


class SignUpCompletionForm(FlaskForm):

    email = HiddenField()
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    country = SelectField('Country', validate_choice=False)
    city = StringField('City', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    bio = TextAreaField('Bio')
    identification_type = SelectField('Id. type', choices=IDENTIFICATION_TYPE_CHOICES, validators=[DataRequired()])
    identification_number = StringField('Id. number', validators=[DataRequired()])
    phone = StringField('Phone')
    submit = SubmitField('Create account')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class ProfileForm(FlaskForm):

    LANGUAGE_CHOICES = [
        ('-1', 'Select languages')
    ]

    country = SelectField('Country', validate_choice=False)
    city = StringField('City', validators=[DataRequired()])
    picture = FileField('Profile picture', validators=[FileAllowed(['jpg', 'png'])])
    languages = SelectMultipleField('Languages', choices=LANGUAGE_CHOICES, coerce=int)
    name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    bio = TextAreaField('Bio')
    identification_type = SelectField('Id. type', choices=IDENTIFICATION_TYPE_CHOICES, validators=[DataRequired()])
    identification_number = StringField('Id. number', validators=[DataRequired()])
    phone = StringField('Phone')
    submit = SubmitField('Save changes')
