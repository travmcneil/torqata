import base64
from datetime import datetime, timedelta
import os
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

class User(UserMixin, PaginatedAPIMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Movies(PaginatedAPIMixin, db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.String(128))
    title = db.Column(db.String(64), index=True)
    type = db.Column(db.String(64), index=True)
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

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.title,
            'type': self.type,
            'director': self.director,
            'cast': self.cast,
        }
        return data

    def from_dict(self, data):
        for field in ['title', 'type', 'director', 'cast',
                        'country', 'rating', 'duration',
                        'listed_in' , 'description']:
            if field in data:
                setattr(self, field, data[field])
    

class Reviews(db.Model):
    __tablename__='review'
    id = db.Column(db.Integer, primary_key=True)
    comments = db.Column(db.Text)
