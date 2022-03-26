import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

APP_NAME = os.environ.get('APP_NAME') or 'Flask API'

# Flask application configuration
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'itsasecret'

# Email address for admin
MAIL_ADMIN = os.environ.get('MAIL_ADMIN')

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Email server configuration
MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
MAIL_SERVER=os.environ.get('MAIL_SERVER')
MAIL_PORT=os.environ.get('MAIL_PORT')
MAIL_USE_SSL=os.environ.get('MAIL_USE_SSL')

# Logging level
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL') or 'DEBUG'
