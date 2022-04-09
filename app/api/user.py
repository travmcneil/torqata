from flask import jsonify, request, url_for, abort
from app import db
from app.models import User, Movies
from app.api import bp
from app.api.auth import token_auth, basic_auth, token_auth_error
from app.api.errors import bad_request


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    user = User.query.get(id)
    print(user.id)
    return jsonify(user.to_dict())


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        abort(403)
    user = User.query.get(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/movies/<int:id>', methods=['GET'])
@token_auth.login_required
def get_movie(id):
    return jsonify(Movies.query.get(id).to_dict())

@bp.route('/movies', methods=['GET'])
@token_auth.login_required
def get_movies():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Movies.to_collection_dict(Movies.query, page, per_page, 'api.get_movies')
    return jsonify(data)

@bp.route('/movies', methods=['POST'])
@token_auth.login_required
def create_movie():
    data = request.get_json() or {}
    movie = Movies()
    movie.from_dict(data, new_user=True)
    db.session.add(movie)
    db.session.commit()
    response = jsonify(movie.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_movies', id=movie.id)
    return response

@bp.route('/movies/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_movie(id):
    if token_auth.current_user().id != id:
        abort(403)
    movie = Movies.query.get(id)
    data = request.get_json() or {}
    movie.from_dict(data, new_movie=False)
    db.session.commit()
    return jsonify(movie.to_dict())
