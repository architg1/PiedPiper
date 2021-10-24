from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, resalepriceinputform
from flask_login import current_user, login_user
from app.models import User, resaleInput
from flask_login import logout_user
from flask_login import login_required
from flask import request
import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/login', methods=['GET', 'POST']) #login page url
def login():
    """
    Summary of function:

    Receives input from LoginForm and checks for valid user in login database

    Returns:

    if successful, redirect to home page
    if unsuccessful, print Invalid username or password redirect back to login page
     
     
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('loginUI.html', title='Sign In', form=form)



def check_password(self, password):
    """
    Summary of function:

    Receives input from LoginForm and checks for valid matching password

    Returns:
    TRUE if match
    FALSE if do not match
     
    """
    return check_password_hash(self.password_hash, password)