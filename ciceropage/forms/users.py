from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from ciceropage.models import User


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('An account already exists for this email address. Please use another one.')


class SignUpCompletionForm(FlaskForm):

    IDENTIFICATION_TYPE_CHOICES = [
        ('cc', 'CC'),
        ('passport', 'Passport'),
        ('nit', 'Nit')
    ]

    email = HiddenField()
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    country = SelectField('Country', validate_choice=False)
    region = SelectField('State/Region', choices=[(-1, 'Select a region')], validate_choice=False)
    city = SelectField('City', choices=[(-1, 'Select a city')], validators=[DataRequired()], coerce=int, validate_choice=False)
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

    IDENTIFICATION_TYPE_CHOICES = [
        ('cc', 'CC'),
        ('passport', 'Passport'),
        ('nit', 'Nit')
    ]

    country = SelectField('Country', validate_choice=False)
    region = SelectField('State/Region', choices=[(-1, 'Select a region')], validate_choice=False)
    city = SelectField('City', choices=[(-1, 'Select a city')], validators=[DataRequired()], coerce=int, validate_choice=False)
    picture = FileField('Profile picture', validators=[FileAllowed(['jpg', 'png'])])
    name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    bio = TextAreaField('Bio')
    identification_type = SelectField('Id. type', choices=IDENTIFICATION_TYPE_CHOICES, validators=[DataRequired()])
    identification_number = StringField('Id. number', validators=[DataRequired()])
    phone = StringField('Phone')
    submit = SubmitField('Save changes')
