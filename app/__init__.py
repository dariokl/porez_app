from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

from config import config
from apscheduler.schedulers.background import BackgroundScheduler




db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
admin = Admin()
migrate = Migrate()



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Itialize databse
    db.init_app(app)
    db.app = app
    migrate.init_app(app, db)

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


    from .users.views import scheduled_cleaning

    scheduler = BackgroundScheduler(daemon=False)
    scheduler.add_job(scheduled_cleaning, 'interval', minutes=5)
    scheduler.start()

    db.create_all()

    return app

