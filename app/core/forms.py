from wtforms import FieldList, FormField, StringField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class FieldEnteryForm(FlaskForm):
    name = StringField()

class FieldsForms(FlaskForm):
    """A form for one or more addresses"""
    fields = FieldList(FormField(FieldEnteryForm), min_entries=1)
    submit = SubmitField('Unesi podatke')

class NekretnineForms(FlaskForm):
    fields = FieldList(FormField(FieldEnteryForm), min_entries=1)
    select = SelectField('Select', choices=[('(kuca)', 'Izaberite nekretninu'), ('(poslovni)', 'Poslovni prostor')], validators=[DataRequired()])
    submit = SubmitField('Select')



