from app.models import User
from flask import flash, redirect, url_for
from flask_login import current_user

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import Email, Regexp, EqualTo, ValidationError, DataRequired, Length

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
    jmbg = StringField('JMBG', validators=[DataRequired(), Length(min=13), Regexp('^[0-9]*$', message="Samo brojevi su dozvoljeni")])
    grad = StringField('Grad', validators=[DataRequired()])
    submit1 = SubmitField('Snimi')

class ProfileEditContact(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    kontakt_tel = IntegerField('Broj Telefona', validators=[DataRequired()])
    submit2 = SubmitField('Snimi')


class ProfileDelete(FlaskForm):
    confirm = PasswordField('Ukucajte šifru svog profila')
    submit3 = SubmitField('Obrisi Profil')

