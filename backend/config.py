import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'krushivaani.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ADD THIS LINE for the login system's security
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'a-super-secret-jwt-key')