from wtforms import FieldList, FormField, StringField, SubmitField
from flask_wtf import FlaskForm


class FieldEnteryForm(FlaskForm):
    name = StringField()

class FieldsForms(FlaskForm):
    """A form for one or more addresses"""
    fields = FieldList(FormField(FieldEnteryForm), min_entries=1)
    submit = SubmitField('Unesi podatke')