import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or '879dd461d269f89c799c52abf49af8c59477c445849953e4'

    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://c1123652:Team8Team8@csmysql.cs.cf.ac.uk:3306/c1123652_aat_Team8'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'response.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
