from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, user_logged_in, user_logged_out
import datetime

from models import User
from db import db

from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, set_access_cookies,get_current_user

#from blinker import Namespace

#my_signals = Namespace()

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    
    email = request.form.get('email')
    password = request.form.get('password')
    
    #params = {'email':email}
    #user_par = User(**params)
    #token = user_par.get_token()
    #headers = {'Authorization': 'Bearer {}'.format(token)}
    remember = True if request.form.get('remember') else False
    #last_login_at = user_logged_in._get_current_object()

    user = User.query.filter_by(email=email).first()
    
    access_token = create_access_token(identity=user.id)
    print('user', user, 'token', access_token)
    
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    
    # updating token in database
    user.token = access_token
    # updating last login time
    user.last_login_at = datetime.datetime.now()
    user.last_request_at = datetime.datetime.now()
    db.session.commit()
    
    login_user(user, remember=remember)
    
    response = make_response(redirect(url_for('main.profile')))
    #response.set_cookie('access_token', access_token) - another way to set cookie. Leave it her for now
    
    #response = jsonify({"msg": "login successful"})
    set_access_cookies(response, access_token)
    
    return response


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    params = {'email':email, 'username':username, 'password':password}
    user_par = User(**params)
    token = user_par.get_token()
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password.
    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'), token=token)
    
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('auth.login'))


@auth.route('/logout')
#@login_required
@jwt_required()
def logout():
    logout_user()
    
    #user = User.query.filter_by(email=get_jwt_identity()).first()
    get_current_user().last_request_at = datetime.datetime.now()
    db.session.commit()
    
    return redirect(url_for('main.index'))

@auth.route('/test', methods=['GET', 'POST'])
@jwt_required()
def test():
    #print(get_current_user())
    #email = get_jwt_identity()
    #user = User.query.filter_by(email=get_jwt_identity()).first()
    #print(email)#, user)
    get_current_user().last_request_at = datetime.datetime.now()
    db.session.commit()
    return 'test passed'
