from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.String(128))
    title = db.Column(db.String(64), index=True)
    type = db.Column(db.String(64), index=True)
    title = db.Column(db.String(128), index=True)
    director = db.Column(db.String(128), index=True)
    cast = db.Column(db.Text)
    country = db.Column(db.String(128))
    date_added = db.Column(db.DateTime, index=True)
    release_year = db.Column(db.DateTime, index=True)
    rating = db.Column(db.String(64))
    duration = db.Column(db.String(128), index=True)
    listed_in = db.Column(db.String(128), index=True)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Title> {self.title}>'

class Reviews(db.Model):
    __tablename__='review'
    id = db.Column(db.Integer, primary_key=True)
    comments = db.Column(db.Text)
