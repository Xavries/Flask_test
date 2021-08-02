from datetime import datetime
from flask_login import UserMixin
from init_app_db import db
from flask_restful import fields


class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

likes_fields = {
    'title' : fields.String,
    'likes_today' : fields.Integer,
}

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default = datetime.now())
    likes = db.relationship('PostLike', backref=db.backref('post'), lazy='dynamic')
    today = db.Column(db.String(100))
    likes_today = db.Column(db.Integer(), default = 0)
    
    def __repr__(self):
        return f'<Post id:{self.id}, title: {self.title}>'

post_fields = {
    'id' : fields.Integer,
    'title' : fields.String,
    'body' : fields.String,
    'created' : fields.DateTime,
    'today' : fields.String,
    'likes_today' : fields.Integer
}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    last_login_at = db.Column(db.DateTime())
    last_request_at = db.Column(db.DateTime())
    liked = db.relationship('PostLike', foreign_keys='PostLike.user_id',
                            backref=db.backref('users'), lazy='dynamic')
    
    # this method is already defined with UserMixin
    # and right now it is using user id to load user
    # it needs to be redefined to use alternative token instead of user id
    def get_id(self):
        return str(self.token)
    
    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(PostLike.user_id == self.id, PostLike.post_id == post.id).count() > 0
        
    
user_fields = {
    'id' : fields.Integer,
    'email' : fields.String,
    'username' : fields.String,
    'password' : fields.String,
    'last_login_at' : fields.DateTime,
    'last_request_at' : fields.DateTime,
}
