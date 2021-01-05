from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField, SelectField, HiddenField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired


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
    pictures = MultipleFileField('Pictures')
    submit = SubmitField('Save')


class ReviewForm(FlaskForm):
    rating = HiddenField(validators=[DataRequired(), NumberRange(1, 5)])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post')