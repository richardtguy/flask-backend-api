from flask import request

from app import db
from app.models import User
from app.api import bp
from app.api.errors import bad_request, error_response
from app.api.auth import token_auth
from app.api.email import send_password_reset_email

import logging
logger = logging.getLogger(__name__)

@bp.route("/passwords", methods=["PUT"])
@token_auth.login_required(optional=True)
def reset_password():
	authenticated_user = token_auth.current_user()
	u = request.args.get('u')
	user = User.query.filter_by(username=u).first()
	if authenticated_user is None:
		#request for password reset
		send_password_reset_email(user)
		return '', 202
	elif authenticated_user is user:
		#update password
		data = request.get_json()
		if data and data['password']:
			user.set_password(data['password'])
			db.session.commit()
			return '', 203
		else:
			return bad_request('must include new password')
	else:
		#user is authenticated but trying to set password for a different user
		return error_response(401)
