from app.models import User
from flask import flash
from flask_login import current_user

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import Email, Required, EqualTo, ValidationError, DataRequired

class RegistrationForm(FlaskForm):
    ime = StringField('Ime' , validators=[DataRequired()])
    prezime = StringField('Prezime', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Ukucajte lozinku', validators=[DataRequired(), EqualTo('confirm_pass', message='Lozinke moraju biti iste !')])
    confirm_pass = PasswordField('Ponovite lozinku', validators=[DataRequired()])
    grad = StringField('Grad', validators=[DataRequired()])
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
    submit = SubmitField('POŠALJI ZAHTJEV')

class PasswordChange(FlaskForm):
    password = PasswordField('Ukucajte lozinku', validators=[EqualTo('confirm_pass', \
                                                                     message='Lozinke moraju biti iste !')])
    confirm_pass = PasswordField('Ponovite lozinku', validators=[DataRequired()])
    submit= SubmitField('PROMJENA LOZINKE')

class ProfileEditPersonal(FlaskForm):
    ime = StringField('Ime' , validators=[DataRequired()])
    prezime = StringField('Prezime', validators=[DataRequired()])
    jmbg = IntegerField('JMBG', validators=[DataRequired()])
    grad = StringField('Grad', validators=[DataRequired()])
    submit = SubmitField('Snimi')

class ProfileEditContact(FlaskForm):
    email = StringField('Email', validators=[Email()])
    kontakt_tel = IntegerField('Broj Telefona')
    submit = SubmitField('Snimi')




class ProfileDelete(FlaskForm):
    submit = SubmitField('Obrisi Profil')
