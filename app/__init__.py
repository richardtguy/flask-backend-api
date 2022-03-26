import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

import logging
logging.basicConfig(level=logging.DEBUG, filename='log')

# extensions
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

# application factory
def create_app():
	app = Flask(__name__)
	app.config.from_pyfile('config.py')

	# initialise extensions
	db.init_app(app)
	migrate.init_app(app, db)
	mail.init_app(app)

	# register blueprints
	from app.api import bp as api_bp
	app.register_blueprint(api_bp, url_prefix='/api')
	from app.password_reset import bp as pw_reset_bp
	app.register_blueprint(pw_reset_bp)

	return app
