from dotenv import load_dotenv
load_dotenv()


import os
from dotenv import load_dotenv

load_dotenv()

# Used to create SQLite database for development and testing purpouses
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    """ Main configuration class is using os.environ to get values from .env file make sure you set up all
     required env variables in order to make application run , also adding any additional functionality
     should be handled with .env variables in order to keep application safe and avoid possible security risks"""

    MAIL_SERVER = os.environ.get('SENDGRID_SERVER')
    MAIL_PORT = (os.environ.get('MAIL_PORT'))
    USE_MAIL_TLS = os.environ.get('USE_MAIL_TLS' or 'True')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_SENDER')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev-database.sqlite')

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}