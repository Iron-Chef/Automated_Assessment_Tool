from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config
import pymysql
import os

app = Flask(__name__)
app.config.from_object(Config)

#basedir = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://c1123652:Team8Team8@csmysql.cs.cf.ac.uk:3306/c1123652_aat_Team8'
#SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir,'project.db')
#SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models