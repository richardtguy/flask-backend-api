from flask_mail import Message
from flask import render_template, current_app
from app import mail, db

import logging
logger = logging.getLogger(__name__)

def send_password_reset_email(user):
	"""Send password reset email to user
	"""
	token = user.get_token(scope='password', expires_in=600)
	send_email(
		'Reset Your Password',
		sender=current_app.config['MAIL_ADMIN'],
		recipients=[user.email],
		text_body=render_template('email/reset_password.txt', user=user, token=token, app=current_app.config['APP_NAME']),
		html_body=render_template('email/reset_password.html', user=user, token=token, app=current_app.config['APP_NAME'])
	)
	db.session.commit()

def send_email(subject, sender, recipients, text_body, html_body):
	"""Send email
	"""
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	mail.send(msg)
