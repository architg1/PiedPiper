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

@app.route('/townrecommender/<username>', methods=['GET', 'POST'])
@login_required
def townrecommender(username):
    """
    Summary of function:

    Receives input from user input history of town predictor input form and outputs
    the recommender town using random forest algorithm from sklearn

    Parameters:
    Username of user who wants to use this machine learning function

    Returns:

    Outputs final recommended town and stores in corresponding database of user
     
     
    """
    df = pd.read_csv("resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv")
    df['remaining_years'] = 100 - (2022 - df['lease_commence_date'])
    overall_df = df[['town', 'flat_type','storey_range','floor_area_sqm','remaining_years', 'resale_price']]
    user = User.query.filter_by(username=username).first_or_404()
    form = townForm()
    if form.validate_on_submit():
        price = form.budget.data
        flat = form.flatType.data
        storey = form.storey.data
        floor = form.floorArea.data
        years = form.age.data
        data = {'town':[0],
        'flat_type':[flat],
       'storey_range':[storey],
       'floor_area_sqm':[floor],
       'remaining_years':[years],
       'resale_price':[price]}
        user_df = pd.DataFrame(data)
        final_df = user_df.append(overall_df)
        final_df.iloc[0]
        final_df['town'] = final_df['town'].astype('category')
        final_df['town_cat'] = final_df['town'].cat.codes
        final_df['flat_type'] = final_df['flat_type'].astype('category')
        final_df['flat_type_cat'] = final_df['flat_type'].cat.codes
        final_df['storey_range'] = final_df['storey_range'].astype('category')
        final_df['storey_range_cat'] = final_df['storey_range'].cat.codes
        ml_df = final_df.iloc[1:,:]
        train, test = train_test_split(ml_df, test_size=0.2, random_state = 4)
        train_x = np.asanyarray(train[['flat_type_cat','storey_range_cat','floor_area_sqm','resale_price']])
        train_y = np.asanyarray(train[['town_cat']])
        test_x = np.asanyarray(test[['flat_type_cat','storey_range_cat','floor_area_sqm','resale_price']])
        test_y = np.asanyarray(test[['town_cat']])
        RF = RandomForestClassifier(n_estimators=50, random_state=0,max_depth=10)
        RF.fit(train_x, train_y.ravel())
        pred_y = RF.predict(test_x)
        round(RF.score(train_x,train_y), 4)
        print("Accuracy:",metrics.accuracy_score(test_y, pred_y))
        user_info = np.asanyarray(final_df[['flat_type_cat','storey_range_cat','floor_area_sqm','resale_price']])
        final_value = RF.predict(user_info)
        final_value[0]
        criteria = (final_df['town_cat'] == final_value[0])
        town = final_df.loc[criteria]
        town_df = town["town"]
        resultFinal = town_df.iloc[0]
        result1 = resultFinal  # PLACEHOLDER, UPDATE WITH MACHINE LEARNING
        tinput = townInput(flatType=form.flatType.data, floorArea=form.floorArea.data,
                           storey=form.storey.data, age=form.age.data, budget=form.budget.data, OUTPUT1=result1, user_id=user.id)
        db.session.add(tinput)
        db.session.commit()
        return redirect(url_for('recommend', username=username, output1=result1))
    return render_template('townrecommender.html', user=user, form=form)