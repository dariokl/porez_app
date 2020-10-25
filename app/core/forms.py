from wtforms import FieldList, FormField, StringField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class FieldEnteryForm(FlaskForm):
    name = StringField(DataRequired())

class FieldsForms(FlaskForm):
    """A form for one or more addresses"""
    fields = FieldList(FormField(FieldEnteryForm), min_entries=1)
    select = SelectField('Izaberite Općinu', choices=[])
    select_y = SelectField('Godina', choices=[])

    submit = SubmitField('Unesi Podatke')

class NekretnineForms(FlaskForm):
    kal_godina = StringField('Porezna godina')
    adresa = StringField('Adresa')
    kanton = StringField('Kanton')
    racun =  StringField('Broj bankovnog racuna')
    banka = StringField('Banka')
    select = SelectField('Select', choices=[('(kuca)', 'Kuca ili stan'), ('(poslovni)', 'Poslovni prostor')], validators=[DataRequired()])
    submit = SubmitField('Unesi Podatke')



