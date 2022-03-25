"""
Database model definitions
"""
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timedelta
import jwt
import logging
import uuid
from app import db

logger = logging.getLogger(__name__)

class User(db.Model):
    """
    Database model for user accounts
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    active_token = db.Column(db.String(36))
    token_expiration = db.Column(db.DateTime)

    def set_password(self, password):
    	self.password_hash = generate_password_hash(password)

    def check_password(self, password):
    	return check_password_hash(self.password_hash, password)

    def get_token(self, scope='users', expires_in=3600):
        now = datetime.utcnow()
        id = uuid.uuid4().hex
        self.active_token = id
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        token = {'token_id': id, scope: self.id, 'exp': now + timedelta(seconds=expires_in)}
        return jwt.encode(token, current_app.config['SECRET_KEY'], algorithm='HS256')

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def verify_token(token, scope='users'):
        # verify signed token has the given scope and is active
        user = None
        try:
            token = jwt.decode(token, current_app.config['SECRET_KEY'],
            								algorithms=['HS256'])
            id = token.get(scope)
            user = User.query.get(id)
            if not user.active_token or \
                (token.get('token_id') != user.active_token) or \
                (user.token_expiration < datetime.utcnow()):
                return None
        except:
            return None
        return user

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def __repr__(self):
    	return '<User {}>'.format(self.username)
