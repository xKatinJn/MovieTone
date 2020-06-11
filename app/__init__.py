import os
from config import Config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import  Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'app/static/img/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['MAX_CONTENT_PATH'] = 12000000
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = '/sign'

from app import routes, models
