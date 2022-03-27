import unittest

from app import create_app, db
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
