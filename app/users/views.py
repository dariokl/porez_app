from flask import url_for, request, render_template, redirect, flash, Markup, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from app import db
from . import users

from ..models import User, Tax
from app.users.forms import RegistrationForm, LoginForm, PasswordReset, PasswordChange, ProfileEditPersonal, \
    ProfileEditContact, ProfileDelete, SubmitJMBG

from ..email import send_email

from datetime import datetime, timedelta

import maya





@users.route('/login', methods=['POST', 'GET'])
def login():
    """ Login authorization will be handled by flask_login package , it will generate user_id withing flask session"""
    form = LoginForm()

    if form.validate_on_submit():
        # Query user table with email data sent by post request after submiting and form validation.
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash(Markup('Vaša email adresa nije registrovana molimo Vas  da izvršite registraciju , kliknite link <a href="/register" class="alert-link">here</a>!'))
            return redirect(url_for('users.login'))

        # Checking the user query , if there is an user registered with the submited email adress
        # We proceed to check his password with verify_password method
        if user is not None and user.verify_password(form.password.data):
            # Using flask_login
            login_user(user)
            flash('Uspješno ste se logovali !')

            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('users.profile')
            return redirect(next)
        flash('Pogrešna lozinka ili email !')

    return render_template('users/login.html', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Uspješno ste se odjavili !")
    return redirect(url_for(('core.index')))


@users.route('/register', methods=['POST', 'GET'])
def register():
    """ Here we are using Flask_WTF to generate forms to make sure our form validation is handled by back end
    after user makes the post request we check if the form is validated and we proceed to create a new user
    for our database"""
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(ime=form.ime.data, prezime=form.prezime.data, password=form.password.data,
                        email=form.email.data, grad=form.grad.data)
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_confirm_token()
        send_email(new_user.email, 'Dobrodošli !',
                   'email/register_email', user=new_user, token=token)
        flash('Da bi ste uspješno završili registraciju molimo Vas provjerite svoj email i izvršite potvrdu email adrese !')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form)


@users.route('/confirm/<token>')
@login_required
def account_confirm(token):
    """ Server side token checking , we use confirm_token to read the token data and change user.is_confirmed to True
    and make the database changes"""

    # Current_user can only be a logged in user because we set the @login_required decorator and if the current user is
    # confirmed we just redirect him to the index page.
    if current_user.is_confirmed:
        return redirect(url_for('core.index'))

    if current_user.confirm_token(token):
        # Checking the data inside the token with .confirm_token method from user class
        db.session.commit()
        flash('Uspješno ste potvrdili Vašu email adresu')
    else:
        flash('Vaš zahtjev nije validan !')

    return redirect(url_for('core.index'))


@users.route('/password-reset', methods=["POST", "GET"])
def password_reset():
    """ A route to request password reset token on users email adress"""
    form = PasswordReset()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.generate_password_reset_token()

        send_email(user.email, 'Izmjena lozinke',
                   "email/password_reset", user=user, token=token)
        flash('Molimo Vas provjerite vašu email adresu !')

        return redirect(url_for('core.index'))

    return render_template('password_reset.html', form=form)


@users.route('/password-change/<token>', methods=["POST"])
def password_change(token):
    """  After the user clicks on the link in email we use @staticmethod from user model which reads the data in token
    data in token is the users id , i do the query over the model and return that user model and proceed to use
    set_password method to change the password """

    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('core.index'))
    form = PasswordChange()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Uspješno ste promijenili lozinku')
        return redirect(url_for('users.login'))
    return render_template('users/password_reset.html', form=form)


@users.route('/email-confirm-token')
@login_required
def email_confirm_token():
    send_email(current_user.email, 'Potvrdite Email Adresu !',
               'email/register_email', user=current_user, token=current_user.generate_confirm_token())
    flash('Provjerite Vašu email adresu i potvrdite svoj račun !')

    return redirect(url_for('users.profile', user_id=current_user.id))
    send_email(current_user.email, 'Potvrdite Email Adresu',
               'email/register_email',)


@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """This view is used for personal profile page , users should have ability to edit the pesonal data. Ability
    to change email address and delete they're own accounts"""

    # We simply check does user exist and return 404 if the user.id is not valid
    user = User.query.filter_by(id=current_user.id).first_or_404()
    porez = Tax.query.all()


    if user != current_user:
        return 403

    # Two forms that we use for personal data changes so as the contact information changes
    form_personal = ProfileEditPersonal()
    form_contact = ProfileEditContact()
    form_delete = ProfileDelete()

    if request.method == 'POST':

        if form_personal.submit1.data and form_personal.validate():
            # Changing the personal data , it does not require any aditional information
            user.ime = form_personal.ime.data
            user.prezime = form_personal.prezime.data
            user.grad = form_personal.grad.data
            user.jmbg = form_personal.jmbg.data
            db.session.commit()
            flash('Uspješno ste promijenili vaše podatke')
            return redirect(url_for('users.profile'))

        if form_contact.submit2.data and form_contact.validate():
            # Validation method outside the form , if current user requires change of his personal contact information
            # Using if statement to check is there an email already used by someone else beacuse we cant user validate
            # email from our form.py
            if current_user.email == form_contact.email.data:
                if current_user.kontakt_tel != form_contact.kontakt_tel.data:
                    user.kontakt_tel = form_contact.kontakt_tel.data
                    db.session.commit()
                    flash('Uspjesno ste ažurirali Vaš broj telefona !')
            else:
                try:
                    validate = User.query.filter_by(
                        email=form_contact.email.data).first()
                    if validate.id != current_user.id:
                        flash('Email je već u upotrebi !')
                        return redirect(url_for('users.profile'))
                except AttributeError:
                    # Create a token that contains email adress , check the email_change_token method to see what happens in view.
                    #token = user.email_change_token(form_contact.email.data, form_contact.kontakt_tel.data)
                    flash(
                        'Da bi ste izvršili promjenu email adrese , provjerite vašu email adresu i izvršite potvrdu !')
                    #send_email(current_user.email, 'Potvrdite promjenu email adrese', 'email/email_change', user=user, token=token)
                    return redirect(url_for('users.profile'))

            return redirect(url_for('users.profile'))

        if form_delete.submit3.data and form_delete.validate():
            if user.verify_password(form_delete.confirm.data):
                db.session.delete(user)
                db.session.commit()
                flash('Uspjesno ste izbrisali svoj profil')
                return redirect(url_for('core.index'))
            else:
                Flash('Unijeli ste pogresnu lozinku !')

    return render_template('users/profile.html', user=user, form_personal=form_personal, form_contact=form_contact,
                           form_delete=form_delete)


@users.route('/email-change/<token>')
@login_required
def email_change(token):
    """Checking the token and calling the email_confirm_change method in order to see what is going on under the hood
    chech the modes.py"""

    if current_user.email_confirm_change(token):
        flash('Uspješno ste promijenili vasu adresu')
        logout_user()
        return redirect(url_for('users.login'))
    else:
        flash('Vaš token nije validan , obratite nam se za pomoć !')
        return redirect(url_for('core.index'))


@users.route('/livesearch', methods=['GET', 'POST'])
def livesearch():
    """Ajax call to this route returns jsonified data to generate all the forms based on name of form and date submited
    currently there is week/month/year filter"""
    search = request.json
    date = search.get('date')


        

    # In case that someone doesnt submit filter i was running into value error that used to query all data in model
    if date:

        date = maya.parse(date).datetime()

        query = Tax.query.filter(Tax.user_id==current_user.id).filter(Tax.tip == search.get('name').upper()).all()

        print(query)

        return jsonify({'name': [e.tip for e in query], 'id': [e.id for e in query]})

    
    return jsonify({'date': 'NONE'})


@users.route('/jmbg', methods=['POST', 'GET'])
def jmbg():

    form = SubmitJMBG()

    if form.validate_on_submit():
        current_user.jmbg = form.jmbg.data
        db.session.commit()
        flash('Uspjesno ste unijeli Vas JMBG')
        return redirect(url_for('core.porez'))



    return render_template('users/jmbg.html', form=form)


def scheduled_cleaning():
    day_filter = datetime.utcnow()
    try:
        expired = db.session.query(User).filter(
            User.is_confirmed == False).filter(User.expire < day_filter).delete()
        db.session.commit()
        print('The cron job scheduled every hour deleted {} users'.format(expired))
    except:
        db.session.rollback()
    finally:
        db.session.close()
