import unittest
from datetime import datetime
import json

import flask
import jwt

from app import create_app, db
from app.models import User
from app.api.errors import bad_request

from app.config import Config

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

class UserModelCase(BaseTest):
    def setUp(self):
        super().setUp()
        u = User()
        u.from_dict({
            "username": "test_user",
            "email": "user@example.com",
            "password": "password"
        })
        db.session.add(u)
        db.session.commit()

    def test_password_hashing(self):
        u = User()
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_get_token(self):
        user = User.query.filter_by(username="test_user").first()
        token = jwt.decode(user.get_token(scope="test"), self.app.config['SECRET_KEY'],
            algorithms=['HS256'])
        self.assertTrue(token.get("test")==user.id)

    def test_revoke_token(self):
        user = User.query.filter_by(username="test_user").first()
        user.revoke_token()
        self.assertTrue(datetime.utcnow() > user.token_expiration)

    def test_verify_token(self):
        user = User.query.filter_by(username="test_user").first()
        token = user.get_token(scope="test")
        self.assertTrue(User.verify_token(token, scope="test")==user)
        self.assertFalse(User.verify_token(token)==user)

    def test_to_dict(self):
        user = User.query.filter_by(username='test_user').first()
        self.assertTrue(user.to_dict()['username']=='test_user')
        self.assertFalse(user.to_dict().get('email')=='user@example.com')
        self.assertTrue(user.to_dict(include_email=True).get('email')=='user@example.com')

    def test_from_dict(self):
        u = User()
        u.from_dict({
            "username": "test_user2",
            "email": "user2@example.com",
            "password": "password"
        }, new_user=True)
        db.session.add(u)
        db.session.commit()
        self.assertTrue(User.query.get(u.id).id==u.id)
        u = User()
        self.assertRaises(TypeError, u.from_dict, {}, new_user=True)
        self.assertRaises(TypeError, u.from_dict, {
            "username": "test_user2",
            "email": "user3@example.com",
            "password": "password"
        }, new_user=True)

class ErrorHandlersCase(BaseTest):
    def test_bad_request(self):
        message = 'message'
        response = bad_request(message)
        self.assertTrue(type(response)==flask.wrappers.Response)
        self.assertTrue(response.status_code==400)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(data['message']==message)
        self.assertTrue(data['error']=='Bad Request')

if __name__ == '__main__':
    unittest.main(verbosity=3)
