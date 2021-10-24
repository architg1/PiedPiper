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

@app.route('/flatprice/<username>/<output>')
@login_required
def flatprice(username, output):
    """
    Summary of function:

    Calls flatPrice.html and
    displays result of desired flat price estimator
     
     
    """
    user = User.query.filter_by(username=username).first_or_404()
    output = output
    return render_template('flatprice.html', user=user, output=output)


@app.route('/recommend/<username>/<output1>/<output2>/<output3>')
@login_required
def recommend(username, output1, output2, output3):
    """
    Summary of function:

    Calls recommend.html and
    displays result of town recommender
     
     
    """
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('recommend.html', user=user, output1=output1, output2=output2, output3=output3)


@app.route('/resaleprice/<username>/<output>')
@login_required
def resaleprice(username, output):
    """
    Summary of function:

    Calls resale.html and
    displays result of resale price estimator
     
     
    """
    user = User.query.filter_by(username=username).first_or_404()
    output = output
    return render_template('resale.html', user=user, output=output)