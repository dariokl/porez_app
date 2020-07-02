from .models import User
from flask import flash

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import Email, Required, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    ime = StringField('Ime' , validators=[Required()])
    prezime = StringField('Prezime', validators=[Required()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Ukucajte lozinku', validators=[EqualTo('confirm_pass',\
                                                                     message='Lozinke moraju biti iste')])
    confirm_pass = PasswordField('Ponovite lozinku', validators=[Required()])
    jmbg = IntegerField('JMBG', validators=[Required()])
    kontakt_tel = IntegerField('Broj Telefona')
    grad = StringField('Grad', validators=[Required()])
    submit = SubmitField('Registruj Se')

    # Used to check if the user email exists in the current database and returns ValidationEerror in that case
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            flash('Email already registered')
            raise ValidationError('Email already registered')

    # Used to check if the users username exists in the current database and returns ValidationEerror in that case
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            flash('Username already taken')
            raise ValidationError('Username already taken')

class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Enter')