import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()  # load environment variables from .env if it exists.

class Config(object):
    """Base Config Object"""
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = os.environ.get('JWT_TOKEN_LOCATION','headers')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed