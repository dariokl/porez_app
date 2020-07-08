from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import config


db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
admin = Admin()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Itialize databse
    db.init_app(app)

    # Init login manager
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'

    #Flask mail
    mail.init_app(app)

    # Blueprint imports from separated modules in app structure
    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from .core import core as core_blueprint
    app.register_blueprint(core_blueprint)

    from .models import User

    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))

    return app

