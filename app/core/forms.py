from wtforms import FieldList, FormField, StringField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired

type_n = [('0', 'Izaberite Nekretinu'), ('kuca', 'Kuca , stan ili zgrada'), ('poslovni', 'Poslovni prostor'), \
    ('garaza', 'Garaza koja se izdaje'), ('parking', 'Parking prostor'), ('vozilo', 'Putnicko vozilo'), \
        ('tvozilo' ,'Teretno vozilo'), ('plovni', 'Plovni objekat'), ('letljelica', 'Letljelica u vlasnistvu fizickih lica'), \
            ('stol', 'Stol u kazinu'), ('automat', 'Automat za zabavne igre')]


type_k = [('0', 'Izaberite Kanton'),('USK', 'Unsko-sanski kanton'), ('PK', 'Posavski Kanton'), ('TK', 'Tuzlanski Kanton'), ("ZDK", 'Zenicko-dobojski kanton'), \
    ('BPK', 'Bosansko-podrinjski kanton'), ('SBK', 'Srednjobosanski kanton'), ('HNK', 'Hercegovacko-neretvanski kanton'), ('ZNK', 'Zapadnohercegovacki kanton'), \
        ('KS', 'Kanton Sarajevo'), ('K10', 'Kanton 10')]

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
    kanton = SelectField('Kanton')
    racun =  StringField('Broj bankovnog racuna')
    banka = StringField('Banka')
    select_type = SelectField('aaaaaaaaaaaaaaa', validators=[DataRequired()])
    submit = SubmitField('Unesi Podatke')

    def __init__(self, **kwargs):
        super(NekretnineForms, self).__init__(**kwargs)
        self.select_type.choices = [(i[0], i[1]) for i in type_n]
        self.kanton.choices = [(i[0], i[1]) for i in type_k]


class DeleteTax(FlaskForm):
    password = PasswordField('Unesite vašu lozinku')
    submit = SubmitField('Obriši Prijavu !')
