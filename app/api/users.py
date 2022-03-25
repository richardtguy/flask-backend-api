from flask import jsonify, url_for, request, abort

from app import db
from app.models import User
from app.api import bp
from app.api.errors import bad_request, error_response
from app.api.auth import token_auth
from app.api.email import send_password_reset_email
from app.api.views import submit_new_password

import logging
logger = logging.getLogger(__name__)

@bp.route("/users/<int:id>", methods=["GET"])
@token_auth.login_required
def get_user(id):
	# Return specified user object to any authenticated user
	return jsonify(User.query.get_or_404(id).to_dict())

@bp.route("/users", methods=["GET"])
@token_auth.login_required
def get_user_by_username():
	# Return specified user object to any authenticated user
	username = request.args.get('u')
	user = User.query.filter_by(username=username).first()
	if user:
		return jsonify(user.to_dict())
	else:
		abort(404)

@bp.route("/users", methods=["POST"])
def create_user():
	data = request.get_json() or {}
	# TODO: move this validation to the User model
	if 'username' not in data or 'password' not in data or 'email' not in data:
		return bad_request('must include username, email and password')
	if User.query.filter_by(username=data['username']).first():
		return bad_request('please try a different username')
	user = User()
	user.from_dict(data, new_user=True)
	db.session.add(user)
	db.session.commit()
	response = jsonify(user.to_dict(include_email=True))
	# TODO: Add URI to body of response
	response.status_code = 201
	response.headers['Location'] = url_for('api.get_user', id=user.id)
	return response
