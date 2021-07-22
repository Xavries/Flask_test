from flask import Blueprint, render_template, request, redirect, url_for

from models import Post
from forms import PostForm

from db import db

import datetime


from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_current_user

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
#@login_required
@jwt_required()
def post_create():
    form = PostForm()
    
    if request.method == "POST":
        title = request.form.get('title')
        body = request.form.get('body')
        
        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:
            print("Veryy long traceback")
        return redirect(url_for('posts.post_detail', slug=post.slug))
    
    # writing user request to database
    current_user.last_request_at = datetime.datetime.now()
    db.session.commit()
    
    return render_template('posts/post_create.html', form=form)

@posts.route('/')
def posts_list():
    op = request.args.get('op')
    
    if op:
        posts = Post.query.filter(Post.title.contains(op) |
        Post.body.contains(op))
    else:
        posts = Post.query.order_by(Post.created.desc())
    return render_template('posts/posts.html', posts=posts)
    
    posts = Post.query.all()
    
    if current_user.is_authenticated:
        # writing user request to database
        current_user.last_request_at = datetime.datetime.now()
        db.session.commit()
    
    return render_template('posts/posts.html', posts=posts)

@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug==slug).first()
    
    if current_user.is_authenticated:
        # writing user request to database
        current_user.last_request_at = datetime.datetime.now()
        db.session.commit()
    
    return render_template('posts/post_detail.html', post=post)

@posts.route('/like/<int:post_id>/<action>')
#@login_required
@jwt_required()
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        if post.today != str(datetime.date.today()):
            post.today = str(datetime.date.today())
            post.likes_today = 0
        
        post.likes_today +=1
        current_user.like_post(post)
        current_user.last_request_at = datetime.datetime.now()
        db.session.commit()
    if action == 'unlike':
        post.likes_today -=1
        current_user.unlike_post(post)
        current_user.last_request_at = datetime.datetime.now()
        db.session.commit()
    return redirect(request.referrer)
