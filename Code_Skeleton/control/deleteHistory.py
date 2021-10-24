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

@app.route('/delete/<username>')
@app.route('/delete/<username>/<id>')
@login_required
def delete(username, id):
    """
    Summary of function:

    Delete a particular input and output history from resalePrice estimator of a particular user

    Parameters:
    1. Username of user who wants to delete
    2. ID of entry that is to be deleted
    
    Returns:

    Removes entry from corresponding database and update profile page
     
     
    """
    user = User.query.filter_by(username=username).first_or_404()
    ID = resaleInput.query.filter_by(id=id).first_or_404()
    db.session.delete(ID)
    db.session.commit()
    return render_template('user.html', user=user)


@app.route('/deletebuyer/<username>')
@app.route('/deletebuyer/<username>/<id>')
@login_required
def deletebuyer(username, id):
    """
    Summary of function:

    Delete a particular input and output history from desired flat price estimator of a particular user

    Parameters:
    1. Username of user who wants to delete
    2. ID of entry that is to be deleted
    Returns:

   Removes entry from corresponding database and update profile page
     
     
    """
    user = User.query.filter_by(username=username).first_or_404()
    ID = flatpriceInput.query.filter_by(id=id).first_or_404()
    db.session.delete(ID)
    db.session.commit()
    return render_template('user.html', user=user)


@app.route('/deletetown/<username>')
@app.route('/deletetown/<username>/<id>')
@login_required
def deletetown(username, id):
    """
    Summary of function:

    Delete a particular input and output history from town recommender of a particular user

    Parameters:
    1. Username of user who wants to delete
    2. ID of entry that is to be deleted
    Returns:

    Removes entry from corresponding database and update profile page
     
     
    """
    user = User.query.filter_by(username=username).first_or_404()
    ID = townInput.query.filter_by(id=id).first_or_404()
    db.session.delete(ID)
    db.session.commit()
    return render_template('user.html', user=user)