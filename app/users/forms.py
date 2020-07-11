from app.models import User
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
    grad = StringField('Grad', validators=[Required()])
    submit = SubmitField('REGISTRUJ SE')

    # Used to check if the user email exists in the current database and returns ValidationEerror in that case
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            flash('Email adresa je u upotrebi')
            raise ValidationError('Email adresa je u upotrebi')

class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('LOG IN')


class PasswordReset(FlaskForm):
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('POSALJI ZAHTJEV')

class PasswordChange(FlaskForm):
    password = PasswordField('Ukucajte lozinku', validators=[EqualTo('confirm_pass', \
                                                                     message='Lozinke moraju biti iste')])
    confirm_pass = PasswordField('Ponovite lozinku', validators=[Required()])
    submit= SubmitField('PROMJENA LOZINKE')

class ProfileEditPersonal(FlaskForm):
    ime = StringField('Ime' , validators=[Required()])
    prezime = StringField('Prezime', validators=[Required()])
    jmbg = IntegerField('JMBG', validators=[Required()])
    grad = StringField('Grad', validators=[Required()])
    submit = SubmitField('Snimi')

class ProfileEditContact(FlaskForm):
    email = StringField('Email', validators=[Email()])
    kontakt_tel = IntegerField('Broj Telefona')
    submit = SubmitField('Snimi')

    # Used to check if the user email exists in the current database and returns ValidationEerror in that case
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            flash('Email adresa je u upotrebi')
            raise ValidationError('Email adresa je u upotrebi')

class ProfileDelete(FlaskForm):
    submit = SubmitField('Obrisi Profil')
