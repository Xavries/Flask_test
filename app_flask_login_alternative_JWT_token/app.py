from flask import Flask

from flask_login import LoginManager

#from config import Config
from db import db, app
#from models import User

from flask_track_usage import TrackUsage
from flask_track_usage.storage.sql import SQLStorage

from flask_jwt_extended import JWTManager#, jwt_required, get_jwt_identity

#app = Flask(__name__)

#app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
#db.init_app(app)
#db = SQLAlchemy(app)

jwt = JWTManager(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


# blueprint for auth routes in our app
from auth.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from main import main as main_blueprint
app.register_blueprint(main_blueprint)

from posts.blueprint import posts as posts_blueprint
app.register_blueprint(posts_blueprint, url_prefix='/blog')

from models import *

@login_manager.user_loader
def load_user(token):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    # but we redefined get_id method and now we are using User token instead of user_id
    return User.query.filter_by(token=token).first()


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


if __name__ == "__main__":
    
    track_storage = TrackUsage(app, SQLStorage(db=db))
    app.run()

