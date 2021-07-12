import datetime
import os

from flask import Flask, render_template, redirect, url_for, request

import flask_admin
from flask_admin import AdminIndexView
from flask_admin.form import rules
from flask_admin.contrib.mongoengine import ModelView

from flask_mongoengine import MongoEngine

from flask_security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user

# Create application
app = Flask(__name__)

# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')

app.config['MONGODB_HOST'] = 'mongodb+srv://linp:YnIeVDMDGGMOGbxG@pursucluster.2qgve.mongodb.net/Flask_admin--Flask_security_DB?retryWrites=true&w=majority'
app.config['MONGODB_PORT'] = 27017

# Create models
db = MongoEngine()
db.init_app(app)

# Define mongoengine documents
class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    name = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    tags = db.ListField(db.ReferenceField('Tag'))
    is_active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField('Role'))

class Items(db.Document):
    title = db.StringField(max_length=60)
    text = db.StringField()
    adress = db.StringField(max_length=60)
    pub_date = db.DateTimeField(default=datetime.datetime.now)
    user = db.ReferenceField(User, required=False)

    # Required for administrative interface
    def __unicode__(self):
        return self.title


class Tag(db.Document):
    name = db.StringField(max_length=10)

    def __unicode__(self):
        return self.name


class Comment(db.EmbeddedDocument):
    name = db.StringField(max_length=20, required=True)
    value = db.StringField(max_length=20)
    tag = db.ReferenceField(Tag)


# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Secure Admin View classes, no you can't access admin without role
class AdminViewMethods:
    def is_accessible(self):
        return current_user.has_role('admin')
    
    def inaccessible_callback(self, name, **kwardgs):
        return redirect(url_for('security.login'))#, next=request_url))

class AdminView(AdminViewMethods, ModelView):
    pass

class AdminVwIndHome(AdminViewMethods, AdminIndexView):
    pass

# Create admin
admin = flask_admin.Admin(app, 'url to Index', url='/', index_view=AdminVwIndHome(name='Admin Home'), template_mode='bootstrap3')


# Customized admin views
class UserView(AdminViewMethods, ModelView):
    column_filters = ['name']

    column_searchable_list = ('name', 'password')

    form_ajax_refs = {
        'tags': {
            'fields': ('name',)
        },
        'roles': {
            'fields': ('name',)
        }
    }


class ItemsView(AdminViewMethods, ModelView):
    column_filters = ['adress']

    form_ajax_refs = {
        'user': {
            'fields': ['name']
        }
    }

# Flask views
@app.route('/')
@login_required
def index():
    return render_template("index.html")


if __name__ == '__main__':
    # Add views
    admin.add_view(UserView(User))
    admin.add_view(ItemsView(Items))
    admin.add_view(AdminView(Tag))
    admin.add_view(AdminView(Role))
    
    # Start app
    app.run(debug=True)
