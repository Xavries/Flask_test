from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from models import post_fields, user_fields, User, Post
from flask import render_template, make_response#, request, redirect, url_for
from init_app_db import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_current_user, current_user, verify_jwt_in_request

request_parser = reqparse.RequestParser()

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


class User_details(Resource):
    @marshal_with(user_fields)
    def get(self):
        print(User.query.all())
        users = User.query.all()
        if not users:
            abort(404, message="Can't find users in resource")
        return users
    '''
    @marshal_with(user_fields)
    def put(self):#, new_email, new_username, new_password):
        args = request_parser.parse_args()
        check_user_exist = User.query.filter_by(email=args['email']).first()
        
        if check_user_exist:
            abort(409, message="User already exist")
            
        new_user = User(email=args['email'], username=args['username'], password=args['password'])

        db.session.add(new_user)
        db.session.commit()
        return new_user, 201
    '''

class User_Signup(Resource):
    
    @marshal_with(user_fields)
    def post(self):
        args = user_signup_args.parse_args()
        print(args)
        print(args['email'])
        check_user_exist = User.query.filter_by(email=args['email']).first()
        if check_user_exist:
            abort(409, message="User already exist. Login or try another email.")
        
        new_user = User(email=args['email'], username=args['username'], password=generate_password_hash(args['password'], method='sha256'))
        
        db.session.add(new_user)
        db.session.commit()
        
        return new_user, 201


class User_Login(Resource):
    
    @marshal_with(user_fields)
    def post(self):
        args = user_login_args.parse_args()
        
        login_me = User.query.filter_by(email=args['email']).first()
        print(login_me, login_me.email)
        if not login_me:
            abort(404, message='Please check your login and try again.')
        
        check_password = check_password_hash(login_me.password, args['password'])
        print(check_password)
        if not check_password:
            abort(404, message='Please check your password and try again.')

        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=str(login_me.id), expires_delta=expires)
        print(access_token)
        
        # DELETE later on...
        login_me.token = access_token
        login_me.last_request_at = datetime.datetime.now()
        db.session.commit()
        
        # ...and integrate this
        '''
        response = make_response(redirect(url_for('main.profile')))
        #response.set_cookie('access_token', access_token) - another way to set cookie. Leave it her for now
    
        #response = jsonify({"msg": "login successful"})
        set_access_cookies(response, access_token)
        '''
        
        return {'token': access_token}, 200


def get_identity_if_logedin():
    try:
        verify_jwt_in_request()
        print(verify_jwt_in_request())
        return get_jwt_identity()
    except Exception:
        pass


class Post_get_put(Resource):
    @marshal_with(post_fields)
    def get(self):
        
        check_user = get_identity_if_logedin()
        print(check_user)
        #print(verify_jwt_in_request())
        ################### method get_identity_if_logedin() doesn't see the user anyway. Rework
        if check_user:
            print(get_jwt_identity())
            get_jwt_identity().last_request_at = datetime.datetime.now()
            db.session.commit()
        
        posts = Post.query.all()
        if not posts:
            abort(404, message="Can't find posts in resource")
        print(posts)
        #headers = {'Content-Type': 'text/html'}
        #print(render_template('posts.html', posts=posts))
        #print(make_response(render_template('posts.html', posts=posts), 200, headers))
        return posts
    
    @jwt_required()
    @marshal_with(post_fields)
    def put(self):
        ############ somehow it works via terminal, but return [422 UNPROCESSABLE ENTITY]> {'msg': 'Signature verification failed'}
        ############ when making request from make_requests.py
        current_user = User.query.filter_by(id=get_jwt_identity()).first()
        args = user_posts_args.parse_args()
            
        new_post = Post(title=args['title'], body=args['body'], created=datetime.datetime.now())

        db.session.add(new_post)
        current_user.last_request_at = datetime.datetime.now()
        db.session.commit()
        return new_post, 201
    
class Post_like(Resource):
    
    
    @marshal_with(post_fields)
    @jwt_required()
    def post(self):
        args = request_parser.parse_args()
        post = Post.query.filter_by(id=args['post_id']).first_or_404()
        current_user = User.query.filter_by(id=get_jwt_identity()).first()
        
        if args['like']:
            #post_like
            if post.today != str(datetime.date.today()):
                post.today = str(datetime.date.today())
                post.likes_today = 0
            post.likes_today +=1
            
            
        elif args['unlike']:
            post.likes_today -=1
            #post_unlike
        
        current_user.last_request_at = datetime.datetime.now()
        db.session.commit()
        
        return {post.title: post.likes_today}
    
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

