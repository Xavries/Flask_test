from app import app

from flask import render_template
from flask_security import Security

@app.route('/')
def index():
    return render_template('index.html')

