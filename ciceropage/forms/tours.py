from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField, SelectField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import IntegerField


class TourForm(FlaskForm):

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('hidden', 'Hidden')
    ]

    title = StringField('Title', validators=[DataRequired()])
    thumbnail = FileField('Thumbnail', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', validators=[DataRequired()], choices=STATUS_CHOICES)
    # pictures = MultipleFileField('Pictures')
    submit = SubmitField('Save')


class TourEditForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired()])
    thumbnail = FileField('Thumbnail', validators=[FileAllowed(['jpg', 'png'])])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', validators=[DataRequired()], choices=TourForm.STATUS_CHOICES)
    submit = SubmitField('Save changes')


class ReviewForm(FlaskForm):
    rating = IntegerField(default=3, validators=[DataRequired(), NumberRange(1, 5)])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post')
