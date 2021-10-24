from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, resalepriceinputform
from flask_login import current_user, login_user
from app.models import User, resaleInput
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from app.forms import priceEstimatorForm, townForm
from app.models import flatpriceInput, townInput

@app.route('/user/<username>')
@login_required
def user(username):
    """
    Summary of function:

    calls user.html to display profile page of user

    Parameters:
    Username of profile that is to be displayed

    Returns:

    The profile page displays user's username,
    and all input and output history of resale price estimator,
    desired flat price estimator and town recommender of that user
     
     
    """
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)