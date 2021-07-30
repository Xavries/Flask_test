from flask_restful import reqparse, abort, Api, Resource
from models import post_fields, user_fields
from flask_jwt_extended import JWTManager
from routes import initialize_routes
from init_app_db import app
from models import User
'''
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
'''
api = Api(app)

client = app.test_client()
#request_parser = reqparse.RequestParser()

jwt = JWTManager(app)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

'''
from resource import * #User_details, Post_get_put, User_Login, User_Signup

##
## setup the Api resource routing down here
##
api.add_resource(User_details, '/users')
api.add_resource(User_Signup, '/signup')
api.add_resource(User_Login, '/login')
api.add_resource(Post_get_put, '/posts')
'''

initialize_routes(api)

if __name__ == '__main__':
    app.run(debug=True)
