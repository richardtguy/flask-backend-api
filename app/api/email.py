from flask_mail import Message
from flask import render_template, current_app
from app import mail, db

import logging
logger = logging.getLogger(__name__)

def send_password_reset_email(user):
	"""
	Send password reset email to user
	"""
	token = user.get_token(scope='password')
	send_email(
		'Reset Your Password',
		sender=current_app.config['MAIL_ADMIN'],
		recipients=[user.email],
		text_body=render_template('email/reset_password.txt', user=user, token=token),
		html_body=render_template('email/reset_password.html', user=user, token=token)
	)
	db.session.commit()

def send_email(subject, sender, recipients, text_body, html_body):
	"""
	Send email
	"""
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	mail.send(msg)
