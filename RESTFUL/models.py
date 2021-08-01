from datetime import datetime

import re

from flask_login import UserMixin

from init_app_db import db

from flask_jwt_extended import create_access_token

from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

# func for creating human-readable links
def slugify(strin):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', strin)

class PostLike(db.Model):
    #__table_args__ = {'extend_existing': True}
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
    slug = db.Column(db.String(200), unique = True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default = datetime.now())
    likes = db.relationship('PostLike', backref=db.backref('post'), lazy='dynamic')
    today = db.Column(db.String(100))
    likes_today = db.Column(db.Integer(), default = 0)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()
    
    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)
        else:
            self.slug = str(int(time()))
    
    def __repr__(self):
        return f'<Post id:{self.id}, title: {self.title}>'

post_fields = {
    'id' : fields.Integer,
    'title' : fields.String,
    'slug' : fields.String,
    'body' : fields.String,
    'created' : fields.DateTime,
    #'likes' : db.relationship('PostLike', backref=db.backref('post'), lazy='dynamic')
    'today' : fields.String,
    'likes_today' : fields.Integer
}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    token = db.Column(db.String(250), unique=True)
    active = db.Column(db.Boolean())
    last_login_at = db.Column(db.DateTime())
    last_request_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
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
    'token' : fields.String,
    'active' : fields.Boolean,
    'last_login_at' : fields.DateTime,
    'last_request_at' : fields.DateTime,
    'last_login_ip' : fields.String,
    'current_login_ip' : fields.String,
    'login_count' : fields.Integer
}
