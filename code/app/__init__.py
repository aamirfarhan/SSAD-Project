# Import flask and template operators
from flask import Flask, render_template, session, jsonify
import random 
import string
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from functools import wraps

UPLOAD_FOLDER = 'app/static/uploads'
# Define the WSGI application object
app = Flask(__name__)

# Configurations

app.config.from_object('config')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app.login.controllers import mod_login
from app.datatable.controllers import mod_datatable

app.register_blueprint(mod_login)
app.register_blueprint(mod_datatable)


db.create_all()

if __name__ == "__main__":
    app.run(host='127.0.0.1')
