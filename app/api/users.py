from flask import jsonify, url_for, request, abort

from app import db
from app.models import User
from app.api import bp
from app.api.errors import bad_request, error_response
from app.api.auth import token_auth

import logging
logger = logging.getLogger(__name__)

@bp.route("/users/<int:id>", methods=["GET"])
@token_auth.login_required
def get_user(id):
	"""Return user by id specified in path to any authenticated user
	"""
	return jsonify(User.query.get_or_404(id).to_dict())

@bp.route("/users", methods=["GET"])
@token_auth.login_required
def get_user_by_username():
	"""Return user by username specified in query parameter to any
	authenticated user
	"""
	username = request.args.get('u')
	user = User.query.filter_by(username=username).first()
	if user:
		return jsonify(user.to_dict())
	else:
		abort(404)

@bp.route("/users", methods=["POST"])
def create_user():
	"""Create new user
	"""
	data = request.get_json() or {}
	user = User()
	try:
		user.from_dict(data, new_user=True)
	except TypeError as e:
		return bad_request(', '.join(e.args))
	db.session.add(user)
	db.session.commit()
	uri = url_for('api.get_user', id=user.id)
	user_dict = user.to_dict(include_email=True)
	user_dict.update({'uri': uri})
	response = jsonify(user_dict)
	response.status_code = 201
	response.headers['Location'] = uri
	return response
