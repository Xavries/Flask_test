from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_current_user
from db import db
import datetime

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        # writing user request to database
        current_user.last_request_at = datetime.datetime.now()
        db.session.commit()
    return render_template('index.html')

@main.route('/profile')
#@login_required
@jwt_required()
def profile():
    # writing user request to database
    current_user.last_request_at = datetime.datetime.now()
    db.session.commit()
    return render_template('profile.html', username=current_user.username)
