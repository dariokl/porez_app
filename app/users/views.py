from flask import url_for, request, render_template, redirect, flash
from flask_login import login_user, current_user
from app import db
from . import users

from ..models import User
from ..forms import RegistrationForm, LoginForm



@users.route('/register', methods=['POST', 'GET'])
def register():
    """ Here we are using Flask_WTF to generate forms to make sure our form validation is handled by back end
    after user makes the post request we check if the form is validated and we proceed to create a new user
    for our database"""

    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User (ime=form.ime.data, prezime=form.prezime.data, password=form.password.data,\
                         email=form.email.data, jmbg=form.jmbg.data, kontakt_tel=form.kontakt_tel.data,\
                         grad=form.grad.data)
        db.session.add(new_user)
        db.session.commit()
        flash ('Uspjesno ste se registrovali')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form)


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
