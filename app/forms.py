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

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please us a different username')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please us a different email')