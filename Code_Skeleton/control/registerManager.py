from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from app import app
from app import db
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Summary of function:

    Receives input from Register Form and checks for valid user in login database

    Returns:

    Store corresponding username and password into database userInfo
     
     
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = registerForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

def set_password(self, password):
    """
    Summary of function:

    Receives input from LoginForm and converts string password to hash

    Returns:
    password in hash 
     
    """
    self.password_hash = generate_password_hash(password)

def validate_username(self, username):
    """
    Summary of function:

    checks to see if username already exists in database

    Returns:
    if username already exists, print: Please use a different username
     
    """
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
        raise ValidationError('Please use a different username.')