from flask import Blueprint, render_template, request, redirect, url_for

from models import Post
from forms import PostForm

from app import db

from flask_security import login_required, current_user

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
@login_required
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
    return render_template('posts/posts.html', posts=posts)

@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug==slug).first()
    return render_template('posts/post_detail.html', post=post)

@posts.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)
