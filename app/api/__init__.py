from flask import Blueprint

bp = Blueprint('api', __name__, template_folder='templates')

# import routes
from app.api import users, tokens, passwords
