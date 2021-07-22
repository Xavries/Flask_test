from datetime import datetime, timedelta
from time import time

import re

from flask_login import UserMixin

from db import db

from flask_jwt_extended import create_access_token
#from passlib.hash import bcrypt

# func for creating human-readable links
def slugify(strin):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', strin)

class PostLike(db.Model):
    #__table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

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
    
    '''def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))'''
        
    '''
    # method for creating tokens
    def get_token(self, expire_time=2400):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token
    '''
    
    # this method is already defined with UserMixin
    # and right now it is using user id to load user
    # it needs to be redefined to use alternative token instead of user id
    def get_id(self):
        return str(self.token)
    
    '''
    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).first()
        if not bcrypt.verify(password, user.password):
            raise Exception('Incorrect password')
        return user
        '''
    
    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(PostLike.user_id == self.id, PostLike.post_id == post.id).count() > 0

