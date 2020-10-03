from flask import current_app
from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta

from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import JSON

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """ Defining the user table and using flask_login to keep track on user auth. """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(64))
    prezime = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    jmbg = db.Column(db.String(64))
    kontakt_tel = db.Column(db.Integer)
    grad = db.Column(db.String(64))

    is_confirmed = db.Column(db.Boolean, default=False)
    expire = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, **kwargs):
        self.expire = datetime.utcnow() + timedelta(days=1)
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '{} {}'.format(self.ime, self.prezime)

    @property
    def password(self):
        raise AttributeError("Password is not readable attribute")

    #Method that is used to change password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Simple method to check the users password once is entered on login page
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Generating the token that will be sent over flask-mail up on user registration
    def generate_confirm_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    # Identical method to the one above , simply generate a token that contains users.id
    def generate_password_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token.encode('utf-8'))
        except:
            False

        # Checking if token contains self.id
        if data.get('confirm') != self.id:
            return False

        # If the token self.id matches we change the users is_active to True
        self.is_confirmed = True
        db.session.add(self)
        return True

    @staticmethod
    def verify_reset_password_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
            id = data.get('confirm')
        except:
            return
        return User.query.get(id)


    #Generating email change token that contains a new email adress from the token , i will use this token to handle
    #Phone number changes too
    def email_change_token(self, email, tel, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'email': email, 'tel': tel, 'confirm': self.id}).decode('utf-8')


    def email_confirm_change(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])

        #Trying to decode the token and handling exception
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            False

        #The users.id must be inside the token in order to pass the validation
        if data.get('confirm') != self.id:
            return False

        #This is where we handle the update on the selected users data
        self.email = data.get('email')
        self.kontakt_tel = data.get('tel')
        db.session.commit()

        return True


class Tax(db.Model):

    __tablename__ = 'taxes'

    id = db.Column(db.Integer, primary_key=True)
    json_data = db.Column(JSON)
    tip = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
