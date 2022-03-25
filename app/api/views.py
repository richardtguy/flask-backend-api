from flask import flash, request, redirect, render_template, url_for

from app import db
from app.api import bp
from app.models import User

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def submit_new_password(token):
    user = User.verify_token(token, 'password')
    if not user:
        flash('Password reset link has expired, please try again', 'error')
        return redirect(url_for('api.index'))
    if request.method == "POST":
        user.set_password(request.form['password'])
        db.session.commit()
        flash('Your password has been reset', 'success')
        return redirect(url_for('api.index'))
    return render_template('submit_new_password.html', user=user)

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
