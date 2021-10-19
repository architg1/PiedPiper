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


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='home')


@app.route('/login', methods=['GET', 'POST'])
def login():
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
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/buyer/<username>')
@login_required
def buyer(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('buyer.html', user=user)


@app.route('/seller/<username>')
@login_required
def seller(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('seller.html', user=user)


@app.route('/resalepriceestimator/<username>', methods=['GET', 'POST'])
@login_required
def resalepriceestimator(username):
    df = pd.read_csv(
        "resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv")
    df['remaining_years'] = 100 - (2022 - df['lease_commence_date'])
    overall_df = df[['town', 'flat_type', 'storey_range',
                     'floor_area_sqm', 'remaining_years', 'resale_price']]
    user = User.query.filter_by(username=username).first_or_404()
    form = resalepriceinputform()
    if form.validate_on_submit():
        # MACHINE LEARNING PART ------------------------------------------------------------------------------------------------
        town = form.town.data
        flat = form.flatType.data
        storey = form.storey.data
        floor = form.floorArea.data
        years = form.age.data
        data = {'town': [town],
                'flat_type': [flat],
                'storey_range': [storey],
                'floor_area_sqm': [floor],
                'remaining_years': [years],
                'resale_price': [0]}
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
        ml_df = final_df.iloc[1:, :]
        train, test = train_test_split(ml_df, test_size=0.2, random_state=4)
        regr = linear_model.LinearRegression()
        train_x = np.asanyarray(
            train[['town_cat', 'flat_type_cat', 'storey_range_cat', 'floor_area_sqm', 'remaining_years']])
        train_y = np.asanyarray(train[['resale_price']])
        regr.fit(train_x, train_y)
        test_x = np.asanyarray(
            test[['town_cat', 'flat_type_cat', 'storey_range_cat', 'floor_area_sqm', 'remaining_years']])
        test_y = np.asanyarray(test[['resale_price']])
        test_y_hat = regr.predict(test_x)
        user_info = np.asanyarray(
            final_df[['town_cat', 'flat_type_cat', 'storey_range_cat', 'floor_area_sqm', 'remaining_years']])
        final_value = regr.predict(user_info)
        # MACHINE LEARNING PART ---------------------------------------------------------------------------------------------
        result = int(final_value[0])
        rsinput = resaleInput(town=form.town.data, flatType=form.flatType.data, ogprice=form.ogprice.data,
                              floorArea=form.floorArea.data, storey=form.storey.data, age=form.age.data, OUTPUT=result, user_id=user.id)
        db.session.add(rsinput)
        db.session.commit()
        return redirect(url_for('resaleprice', username=username, output=result))

    return render_template('resalepriceestimator.html', user=user, form=form)


@app.route('/flatpriceestimator/<username>', methods=['GET', 'POST'])
@login_required
def flatpriceestimator(username):
    df = pd.read_csv(
        "resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv")
    df['remaining_years'] = 100 - (2022 - df['lease_commence_date'])
    overall_df = df[['town', 'flat_type', 'storey_range',
                     'floor_area_sqm', 'remaining_years', 'resale_price']]
    user = User.query.filter_by(username=username).first_or_404()
    form = priceEstimatorForm()
    if form.validate_on_submit():
        # MACHINE LEARNING PART ------------------------------------------------------------------------------------------------
        town = form.town.data
        flat = form.flatType.data
        storey = form.storey.data
        floor = form.floorArea.data
        years = form.age.data
        data = {'town': [town],
                'flat_type': [flat],
                'storey_range': [storey],
                'floor_area_sqm': [floor],
                'remaining_years': [years],
                'resale_price': [0]}
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
        ml_df = final_df.iloc[1:, :]
        train, test = train_test_split(ml_df, test_size=0.2, random_state=4)
        regr = linear_model.LinearRegression()
        train_x = np.asanyarray(
            train[['town_cat', 'flat_type_cat', 'storey_range_cat', 'floor_area_sqm', 'remaining_years']])
        train_y = np.asanyarray(train[['resale_price']])
        regr.fit(train_x, train_y)
        test_x = np.asanyarray(
            test[['town_cat', 'flat_type_cat', 'storey_range_cat', 'floor_area_sqm', 'remaining_years']])
        test_y = np.asanyarray(test[['resale_price']])
        test_y_hat = regr.predict(test_x)
        user_info = np.asanyarray(
            final_df[['town_cat', 'flat_type_cat', 'storey_range_cat', 'floor_area_sqm', 'remaining_years']])
        final_value = regr.predict(user_info)
        # MACHINE LEARNING PART ---------------------------------------------------------------------------------------------
        result = int(final_value[0])
        fpinput = flatpriceInput(town=form.town.data, flatType=form.flatType.data, floorArea=form.floorArea.data,
                                 storey=form.storey.data, age=form.age.data, OUTPUT=result, user_id=user.id)
        db.session.add(fpinput)
        db.session.commit()
        return redirect(url_for('flatprice', username=username, output=result))
    return render_template('flatpriceestimator.html', user=user, form=form)


@app.route('/townrecommender/<username>', methods=['GET', 'POST'])
@login_required
def townrecommender(username):
    df = pd.read_csv(
        "resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv")
    df['remaining_years'] = 100 - (2022 - df['lease_commence_date'])
    overall_df = df[['town', 'flat_type', 'storey_range',
                     'floor_area_sqm', 'remaining_years', 'resale_price']]
    user = User.query.filter_by(username=username).first_or_404()
    form = townForm()
    if form.validate_on_submit():
        # MACHINE LEARNING PART ------------------------------------------------------------------------------------------------
        price = form.budget.data
        flat = form.flatType.data
        storey = form.storey.data
        floor = form.floorArea.data
        years = form.age.data
        data = {'town': [0],
                'flat_type': [flat],
                'storey_range': [storey],
                'floor_area_sqm': [floor],
                'remaining_years': [years],
                'resale_price': [price]}
        user_df = pd.DataFrame(data)
        final_df = user_df.append(overall_df)
        final_df.iloc[0]
        final_df['town'] = final_df['town'].astype('category')
        final_df['town_cat'] = final_df['town'].cat.codes
        final_df['flat_type'] = final_df['flat_type'].astype('category')
        final_df['flat_type_cat'] = final_df['flat_type'].cat.codes
        final_df['storey_range'] = final_df['storey_range'].astype('category')
        final_df['storey_range_cat'] = final_df['storey_range'].cat.codes
        ml_df = final_df.iloc[1:, :]
        train, test = train_test_split(ml_df, test_size=0.2, random_state=4)
        train_x = np.asanyarray(
            train[['flat_type_cat', 'storey_range_cat', 'floor_area_sqm', 'resale_price']])
        train_y = np.asanyarray(train[['town_cat']])
        test_x = np.asanyarray(
            test[['flat_type_cat', 'storey_range_cat', 'floor_area_sqm', 'resale_price']])
        test_y = np.asanyarray(test[['town_cat']])
        RF = RandomForestClassifier(
            n_estimators=50, random_state=0, max_depth=10)
        RF.fit(train_x, train_y.ravel())
        pred_y = RF.predict(test_x)
        round(RF.score(train_x, train_y), 4)
        print("Accuracy:", metrics.accuracy_score(test_y, pred_y))
        user_info = np.asanyarray(
            final_df[['flat_type_cat', 'storey_range_cat', 'floor_area_sqm', 'resale_price']])
        final_value = RF.predict(user_info)
        final_value[0]
        criteria = (final_df['town_cat'] == final_value[0])
        town = final_df.loc[criteria]
        town_df = town["town"]
        resultFinal = town_df.iloc[0]
        result1 = resultFinal  # PLACEHOLDER, UPDATE WITH MACHINE LEARNING
        result2 = "SENGKANG"
        result3 = "HOUGANG"
        tinput = townInput(flatType=form.flatType.data, floorArea=form.floorArea.data,
                           storey=form.storey.data, age=form.age.data, budget=form.budget.data, OUTPUT1=result1, OUTPUT2=result2, OUTPUT3=result3, user_id=user.id)
        db.session.add(tinput)
        db.session.commit()
        return redirect(url_for('recommend', username=username, output1=result1, output2=result2, output3=result3))
    return render_template('townrecommender.html', user=user, form=form)


@app.route('/delete/<username>')
@app.route('/delete/<username>/<id>')
@login_required
def delete(username, id):
    user = User.query.filter_by(username=username).first_or_404()
    ID = resaleInput.query.filter_by(id=id).first_or_404()
    db.session.delete(ID)
    db.session.commit()
    return render_template('user.html', user=user)


@app.route('/deletebuyer/<username>')
@app.route('/deletebuyer/<username>/<id>')
@login_required
def deletebuyer(username, id):
    user = User.query.filter_by(username=username).first_or_404()
    ID = flatpriceInput.query.filter_by(id=id).first_or_404()
    db.session.delete(ID)
    db.session.commit()
    return render_template('user.html', user=user)


@app.route('/deletetown/<username>')
@app.route('/deletetown/<username>/<id>')
@login_required
def deletetown(username, id):
    user = User.query.filter_by(username=username).first_or_404()
    ID = townInput.query.filter_by(id=id).first_or_404()
    db.session.delete(ID)
    db.session.commit()
    return render_template('user.html', user=user)


@app.route('/resaleoutput/<username>')
@login_required
def resaleoutput(username):
    return render_template('resaleoutput.html', user=user)


@app.route('/flatprice/<username>/<output>')
@login_required
def flatprice(username, output):
    user = User.query.filter_by(username=username).first_or_404()
    output = output
    return render_template('flatprice.html', user=user, output=output)


@app.route('/recommend/<username>/<output1>/<output2>/<output3>')
@login_required
def recommend(username, output1, output2, output3):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('recommend.html', user=user, output1=output1, output2=output2, output3=output3)


@app.route('/resaleprice/<username>/<output>')
@login_required
def resaleprice(username, output):
    user = User.query.filter_by(username=username).first_or_404()
    output = output
    return render_template('resale.html', user=user, output=output)
