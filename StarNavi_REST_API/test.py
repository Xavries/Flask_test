from flask_restful import Api
from models import post_fields, user_fields
from flask_jwt_extended import JWTManager
from routes import initialize_routes
from init_app_db import app
from models import User

api = Api(app)

client = app.test_client()

jwt = JWTManager(app)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

initialize_routes(api)

if __name__ == '__main__':
    app.run(debug=True)
