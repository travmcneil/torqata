from datetime import datetime
from turtle import width
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError 

from app.models import User

class NewMovieForm(FlaskForm):
    type = StringField('Type')
    title = StringField('Title', validators=[DataRequired()])
    director = StringField('Director')
    cast =TextAreaField('Cast')
    country = StringField('Country')
    date_added = DateField('Date Added', default=datetime.today())
    release_year = DateField('Release Year', default=datetime.today())
    rating = StringField("Rating")
    duration = StringField("Duration")
    listed_in = TextAreaField('Listed In')
    description = TextAreaField('Description')
    submit = SubmitField('Submit')