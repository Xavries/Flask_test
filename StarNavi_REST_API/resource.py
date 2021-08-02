from flask_restful import Resource, reqparse, abort, marshal_with
from models import post_fields, user_fields, likes_fields, User, Post
from init_app_db import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, current_user, verify_jwt_in_request


## signup args
user_signup_args = reqparse.RequestParser()
user_signup_args.add_argument("email", type=str, help="Email is required", required=True)
user_signup_args.add_argument("username", type=str, help="Username is required", required=True)
user_signup_args.add_argument("password", type=str, help="Password is required", required=True)
##

## login args
user_login_args = reqparse.RequestParser()
user_login_args.add_argument("email", type=str, help="Email is required", required=True)
user_login_args.add_argument("password", type=str, help="Password is required", required=True)
##

## posts args
user_posts_args = reqparse.RequestParser()
user_posts_args.add_argument("title", type=str, help="Title is required", required=True)
user_posts_args.add_argument("body", type=str, help="Body")
##

## post like args
like_post_args = reqparse.RequestParser()
like_post_args.add_argument("post_id", type=int, help="Post id is required", required=True)
like_post_args.add_argument("like_unlike", type=str, help="Like of unlike is required", required=True)
##

def get_identity_if_logedin():
    
    try:
        verify_jwt_in_request()
        print(verify_jwt_in_request())
        return get_jwt_identity()
    except Exception:
        pass


def write_request_if_logedin():
    
    check_user = get_identity_if_logedin()

    if check_user:
        current_user = User.query.filter_by(id=check_user).first()
        current_user.last_request_at = datetime.datetime.now()
        db.session.commit()


class User_activity(Resource):
    @marshal_with(user_fields)
    def get(self):
        
        write_request_if_logedin()
        
        users = User.query.all()
        
        if not users:
            abort(404, message="Can't find users in resource")
        
        return users


class User_Signup(Resource):
    
    @marshal_with(user_fields)
    def post(self):
        
        args = user_signup_args.parse_args()
        check_user_exist = User.query.filter_by(email=args['email']).first()
        
        if check_user_exist:
            abort(409, message="User already exist. Login or try another email.")
        
        new_user = User(email=args['email'], username=args['username'], password=generate_password_hash(args['password'], method='sha256'))
        
        db.session.add(new_user)
        db.session.commit()
        
        return new_user, 201


class User_Login(Resource):
    
    #@marshal_with(user_fields)
    def post(self):
        args = user_login_args.parse_args()
        
        login_me = User.query.filter_by(email=args['email']).first()

        if not login_me:
            abort(404, message='Please check your login and try again.')
        
        check_password = check_password_hash(login_me.password, args['password'])

        if not check_password:
            abort(404, message='Please check your password and try again.')
        
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=str(login_me.id), expires_delta=expires)
        
        login_me.last_request_at = datetime.datetime.now()
        login_me.last_login_at = datetime.datetime.now()
        db.session.commit()
           
        return {"msg": "login successful"}, 200, {"Set-Cookie": f"acces_token={access_token}"}


class Post_get_put(Resource):
    @marshal_with(post_fields)
    def get(self):
        
        write_request_if_logedin()
        
        posts = Post.query.all()
        
        if not posts:
            abort(404, message="Can't find posts in resource")

        return posts
    
    @jwt_required()
    @marshal_with(post_fields)
    def put(self):
        
        current_user = User.query.filter_by(id=get_jwt_identity()).first()
        args = user_posts_args.parse_args()
            
        new_post = Post(title=args['title'], body=args['body'], created=datetime.datetime.now())

        db.session.add(new_post)
        current_user.last_request_at = datetime.datetime.now()
        db.session.commit()
        
        return new_post, 201
    
class Post_like(Resource):
    
    @marshal_with(likes_fields)
    def get(self):
        
        write_request_if_logedin()
        
        posts = Post.query.all()
        
        return posts
    
    @marshal_with(post_fields)
    @jwt_required()
    def post(self):
        
        args = like_post_args.parse_args()
        post = Post.query.filter_by(id=args['post_id']).first_or_404()
        current_user = User.query.filter_by(id=get_jwt_identity()).first()
        
        if args['like_unlike']=='like':
            
            if post.today != str(datetime.date.today()):
                post.today = str(datetime.date.today())
                post.likes_today = 0
            
            post.likes_today +=1
            current_user.like_post(post)
            db.session.commit()
            
        elif args['like_unlike']=='unlike':
            
            post.likes_today -=1
            current_user.unlike_post(post)
            db.session.commit()
        
        else:
            abort(404, message="Incorrect parameter in request. Use 'like' or 'unlike' only")
        
        current_user.last_request_at = datetime.datetime.now()
        db.session.commit()
        
        return {post.title: post.likes_today}
