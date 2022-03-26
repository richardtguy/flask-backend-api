from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='templates')

# import routes
from app.password_reset import views
