import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SECURITY_REGISTERABLE = True
    #SECURITY_REGISTER_URL = '/sign_up'
    JWT_SECRET_KEY = SECRET_KEY = os.urandom(16).hex()#'super-secret'
    #SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
    #SECURITY_PASSWORD_HASH = 
    #SECURITY_TRACKABLE = True
    JWT_TOKEN_LOCATION = ['headers', 'query_string', 'cookies'] #'headers', 'query_string', 
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = True 
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
    TRACK_USAGE_COOKIE = True
