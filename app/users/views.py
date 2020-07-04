from flask import url_for, request, render_template, redirect, flash
from flask_login import login_user, current_user, login_required
from app import db
from . import users

from ..models import User
from ..forms import RegistrationForm, LoginForm, PasswordReset, PasswordChange

from ..email import send_email

@users.route('/register', methods=['POST', 'GET'])
def register():
    """ Here we are using Flask_WTF to generate forms to make sure our form validation is handled by back end
    after user makes the post request we check if the form is validated and we proceed to create a new user
    for our database"""

    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(ime=form.ime.data, prezime=form.prezime.data, password=form.password.data, \
                        email=form.email.data, jmbg=form.jmbg.data, kontakt_tel=form.kontakt_tel.data, \
                        grad=form.grad.data)
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_confirm_token()
        send_email(new_user.email, 'Dobrodosli !', 'email/register_email', user=new_user, token=token)
        flash('Uspjesno ste se registrovali')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form)


@users.route('/confirm/<token>')
@login_required
def account_confirm(token):
    """ Server side token checking , we use confirm_token to read the token data and change user.is_confirmed to True
    and make the database changes"""

    #Current_user can only be a logged in user because we set the @login_required decorator and if the current user is
    #confirmed we just redirect him to the index page.
    if current_user.is_confirmed:
        return redirect(url_for('core.index'))

    if current_user.confirm_token(token):
        db.session.commit()
        flash('Uspjesno ste potvrdili vasu email adresu')
    else:
        flash('Vas zahtjev nije validan , pokusajte poslati token ponovo')

    return redirect(url_for('core.index'))


@users.route('/login', methods=['POST', 'GET'])
def login():
    """ Login authorization will be handled by flask_login package , it will generate user_id withing flask session"""
    form = LoginForm()

    if form.validate_on_submit():
        # Query user table with email data sent by post request after submiting and form validation.
        user = User.query.filter_by(email=form.email.data).first()

        # Checking the user query , if there is an user registered with the submited email adress
        # We proceed to check his password with verify_password method
        if user is not None and user.verify_password(form.password.data):
            # Using flask_login
            login_user(user)
            flash('You are logged in')

            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('users.register')
            return redirect(next)
        flash('Wrong username or password')

    return render_template('users/login.html', form=form)


@users.route('/password-reset', methods=["POST", "GET"])
def password_reset():
    """ A route to request password reset token on users email adress"""

    form = PasswordReset()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.generate_password_reset_token()

        send_email(user.email, 'Izmjena lozinke', "email/password_reset", user=user, token=token)
        flash ('Molim vas provjerite vas Inbox vase email adrese')

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
        flash('Your password has been reset.')
        return redirect(url_for('users.login'))
    return render_template('users/password_reset.html', form=form)

@users.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()



    return render_template('users/profile.html', user=user)

