from flask import Flask, render_template
from flask_admin import Admin
from flask_admin import BaseView, expose
#from flask_admin.contrib.pymongo import ModelView
import pymongo
from pymongo_insert import get_database

from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/linp/A_LEARN/flask_admin/ftest.sqlite'
app.config['SECRET_KEY'] = 'secret'
print(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)
# set optional bootswatch theme
#app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='microblog', template_mode='bootstrap3')

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
# Add administrative views here

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

class NotificationsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/notify.html')

admin.add_view(NotificationsView(name='Notifications', endpoint = 'notify'))
admin.add_view(ModelView(Items, db.session))

app.run(debug = True)
