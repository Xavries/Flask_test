from app import app, db
import views
from posts.blueprint import posts

from flask_security import SQLAlchemyUserDatastore, Security
from models import User, Role

from flask_track_usage import TrackUsage
from flask_track_usage.storage.sql import SQLStorage

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

app.register_blueprint(posts, url_prefix='/blog')

if __name__ == "__main__":
    
    track_storage = TrackUsage(app, SQLStorage(db=db))
    app.run()
