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
import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

@app.route('/resalepriceestimator/<username>', methods=['GET', 'POST'])
@login_required
def resalepriceestimator(username):
    """
    Summary of function:

    Receives input from user input history of resalePrice or priceEstimator input form and outputs
    the estimated price using a regression model from sklearn

    Parameters:
    Username of user who wants to use this machine learning function

    Returns:

    Outputs final predicted price and stores in corresponding database of user
     
     
    """
    df = pd.read_csv("resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv")
    df['remaining_years'] = 100 - (2022 - df['lease_commence_date'])
    overall_df = df[['town', 'flat_type','storey_range','floor_area_sqm','remaining_years', 'resale_price']]
    user = User.query.filter_by(username=username).first_or_404()
    form = resalepriceinputform()
    if form.validate_on_submit():
        # MACHINE LEARNING PART ------------------------------------------------------------------------------------------------
        town =form.town.data
        flat = form.flatType.data
        storey = form.storey.data
        floor = form.floorArea.data
        years =form.age.data
        data = {'town':[town],
        'flat_type':[flat],
       'storey_range':[storey],
       'floor_area_sqm':[floor],
       'remaining_years':[years],
       'resale_price':[0]}
        user_df = pd.DataFrame(data)
        final_df = user_df.append(overall_df)
        final_df.iloc[0]
        # need to encode town, flat_type, and storey_range
        final_df['town'] = final_df['town'].astype('category')
        final_df['town_cat'] = final_df['town'].cat.codes
        final_df['flat_type'] = final_df['flat_type'].astype('category')
        final_df['flat_type_cat'] = final_df['flat_type'].cat.codes
        final_df['storey_range'] = final_df['storey_range'].astype('category')
        final_df['storey_range_cat'] = final_df['storey_range'].cat.codes
        # Dataframe for training and testing purposes
        ml_df = final_df.iloc[1:,:]
        train, test = train_test_split(ml_df, test_size=0.2, random_state = 4)
        regr = linear_model.LinearRegression()
        train_x = np.asanyarray(train[['town_cat','flat_type_cat','storey_range_cat','floor_area_sqm','remaining_years']])
        train_y = np.asanyarray(train[['resale_price']])
        regr.fit (train_x, train_y)
        test_x = np.asanyarray(test[['town_cat','flat_type_cat','storey_range_cat','floor_area_sqm','remaining_years']])
        test_y = np.asanyarray(test[['resale_price']])
        test_y_hat = regr.predict(test_x)
        user_info = np.asanyarray(final_df[['town_cat','flat_type_cat','storey_range_cat','floor_area_sqm','remaining_years']])
        final_value = regr.predict(user_info)
        ## MACHINE LEARNING PART ---------------------------------------------------------------------------------------------
        result = int (final_value[0]) 
        rsinput = resaleInput(town=form.town.data, flatType=form.flatType.data, ogprice=form.ogprice.data,
                              floorArea=form.floorArea.data, storey=form.storey.data, age=form.age.data, OUTPUT=result, user_id=user.id)
        db.session.add(rsinput)
        db.session.commit()
        return redirect(url_for('resaleprice', username=username, output=result))

    return render_template('resalepriceestimator.html', user=user, form=form)