import json
from base64 import b64encode
import unittest

from flask.wrappers import Response
import jwt

from app import db
from app.models import User
from app.api.errors import bad_request

from .base import TestConfig
from .base import BaseTest

def _basic_auth_str(username, password):
        creds = f"{username}:{password}".encode('ascii')
        credentials = b64encode(creds).decode("utf-8")
        return credentials

class UserFixture():
    def setUp(self):
        super().setUp()
        self.c = self.app.test_client()
        # create test user and get authentication token
        u = User()
        u.from_dict({
            "username": "test_user",
            "email": "user@example.com",
            "password": "password"
        }, new_user=True)
        db.session.add(u)
        db.session.commit()
        self.u = u
        self.token = u.get_token()

class TokensCase(UserFixture, BaseTest):
    def test_get_token(self):
        # valid request
        r = self.c.post("/api/tokens", headers={
            "Authorization": "Basic " + _basic_auth_str("test_user", "password")
        })
        self.assertTrue(r.status_code==200)
        token = jwt.decode(r.json, self.app.config['SECRET_KEY'],
            algorithms=['HS256'])
        self.assertTrue(token["users"]==self.u.id)
        # invalid request
        r = self.c.post("/api/tokens", headers={
            "Authorization": "Basic " + _basic_auth_str("test_user", "fake")
        })
        self.assertTrue(r.status_code==401)

    def test_revoke_token(self):
        r = self.c.get(f'/api/users/{self.u.id}', headers={
            "Authorization": "Bearer " + self.token
        })
        self.assertTrue(r.status_code==200)
        r = self.c.delete(f'/api/tokens', headers={
            "Authorization": "Bearer " + self.token
        })
        self.assertTrue(r.status_code==204)
        r = self.c.get(f'/api/users/{self.u.id}', headers={
            "Authorization": "Bearer " + self.token
        })
        self.assertTrue(r.status_code==401)

class UsersCase(UserFixture, BaseTest):
    def test_get_user_by_username(self):
        # unauthenticated request
        r = self.c.get(f'/api/users?u={self.u.username}')
        self.assertTrue(r.status_code==401)
        # authenticated request
        r = self.c.get(f'/api/users?u={self.u.username}', headers={
            "Authorization": "Bearer " + self.token
        })
        self.assertTrue(r.status_code==200)
        self.assertTrue(r.json==self.u.to_dict())

    def test_get_user(self):
        # unauthenticated request
        r = self.c.get(f'/api/users/{self.u.id}')
        self.assertTrue(r.status_code==401)
        # authenticated request
        r = self.c.get(f'/api/users/{self.u.id}', headers={
            "Authorization": "Bearer " + self.token
        })
        self.assertTrue(r.status_code==200)
        self.assertTrue(r.json==self.u.to_dict())

    def test_create_user(self):
        raise NotImplementedError

class PasswordsCase(UserFixture, BaseTest):
    def test_reset_password(self):
        raise NotImplementedError

class ErrorHandlersCase(BaseTest):
    def test_bad_request(self):
        message = 'message'
        response = bad_request(message)
        self.assertTrue(type(response)==Response)
        self.assertTrue(response.status_code==400)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(data['message']==message)
        self.assertTrue(data['error']=='Bad Request')
