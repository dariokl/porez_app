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
    SCHEDULER_API_ENABLED = True

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{pw}@{url}/{db}'.format(user=os.environ.get('MYSQL_USER'),
                                                                              pw=os.environ.get(
                                                                                  'MYSQL_PW'),
                                                                              url=os.environ.get(
                                                                                  'MYSQL_URL'),
                                                                              db=os.environ.get('MYSQL_DB'))


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'dev-database.sqlite')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'test.sqlite')

class PostgresConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='dariokl',pw='lolpasspass12',url='localhost:5432',db='porez_test')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'post': PostgresConfig

}
