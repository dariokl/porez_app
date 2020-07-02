from app import db, login_manager
from flask_login import UserMixin

from werkzeug.security import check_password_hash, generate_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):
    """ Defining the user table and using flask_login to keep track on user auth. """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(64))
    prezime = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    jmbg = db.Column(db.Integer)
    kontakt_tel = db.Column(db.Integer)
    grad = db.Column(db.String)


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '{} {}'.format(self.ime, self.prezime)


    @property
    def password(self):
        raise AttributeError("Password is not readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)