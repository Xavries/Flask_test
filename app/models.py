from datetime import datetime
from time import time

import re

from flask_security import UserMixin, RoleMixin

from app import db#, my_signals

# func for creating human-readable links
def slugify(strin):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', strin)

# here many-to-many relationship for Post and Tag defined as a variable
posts_tags = db.Table('posts_tags', 
                        db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')), extend_existing=True)

class PostLike(db.Model):
    #__table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    slug = db.Column(db.String(100), unique = True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default = datetime.now())
    tags = db.relationship('Tag', secondary = posts_tags, backref=db.backref('posts'), lazy='dynamic')
    likes = db.relationship('PostLike', backref=db.backref('post'), lazy='dynamic')
    
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


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = slugify(self.title)
    
    def __repr__(self):
        return f'<Tag id:{self.id}, title: {self.title}>'

# here many-to-many relationship for User and Role defined as a class
class RolesUsers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    active = db.Column(db.Boolean())
    #last_login_at = db.Column(db.DateTime())
    #current_login_at = db.Column(db.DateTime())
    #login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))
    liked = db.relationship('PostLike', foreign_keys='PostLike.user_id',
                            backref=db.backref('users'), lazy='dynamic')

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(PostLike.user_id == self.id, PostLike.post_id == post.id).count() > 0

