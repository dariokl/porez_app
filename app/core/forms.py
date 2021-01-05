from wtforms import FieldList, FormField, StringField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired


class FieldEnteryForm(FlaskForm):
    name = StringField(DataRequired())

class FieldsForms(FlaskForm):
    """
    A form for one or more addresses
    """
    fields = FieldList(FormField(FieldEnteryForm), min_entries=1)
    select = SelectField('Izaberite Općinu', choices=[])
    address = StringField('Adresa Nekretnine')

    submit = SubmitField('Unesi Podatke')

class NekretnineForms(FlaskForm):
    kal_godina = StringField('Porezna godina')
    adresa = StringField('Adresa')
    kanton = StringField('Kanton')
    racun =  StringField('Broj bankovnog racuna')
    banka = StringField('Banka')
    select = SelectField('Select', choices=[('0', 'Izabreite Nekretninu'), ('(kuca)', 'Kuca ili stan'), ('(poslovni)', 'Poslovni prostor')], validators=[DataRequired()])
    submit = SubmitField('Unesi Podatke')


class DeleteTax(FlaskForm):
    password = PasswordField('Unesite vašu lozinku')
    submit = SubmitField('Obriši Prijavu !')
