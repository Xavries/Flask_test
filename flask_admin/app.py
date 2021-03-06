import os
from flask import Flask, render_template, redirect, url_for, request
from flask_admin import Admin, AdminIndexView
from flask_admin import BaseView, expose
#from flask_admin.contrib.pymongo import ModelView
#import pymongo
#from pymongo_insert import get_database

from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore, current_user
from database import db_session, init_db
from models import User, Role

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/linp/A_LEARN/flask_admin/ftest.sqlite'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')

user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)

#@app.before_first_request
def create_user():
    init_db()
    user_datastore.create_user(email='pursu@test.net', password='password')
    db_session.commit()

print(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)
# set optional bootswatch theme
#app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

class AdminViewMethods:
    def is_accessible(self):
        return current_user.has_role('admin')
    
    def inaccessible_callback(self, name, **kwardgs):
        return redirect(url_for('security.login', next=request_url))

class AdminView(AdminViewMethods, ModelView):
    pass

class AdminVwIndHome(AdminViewMethods, AdminIndexView):
    pass

admin = Admin(app, 'url to Index', url='/', index_view=AdminVwIndHome(name='Admin Home'), template_mode='bootstrap3')


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    Address = db.Column(db.String(100))

# Add administrative views here

@app.route("/")
def index():
    return render_template("index.html")

'''
class NotificationsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/notify.html')
admin.add_view(NotificationsView(name='Notifications', endpoint = 'notify'))
'''
admin.add_view(AdminView(Items, db.session))

app.run()
