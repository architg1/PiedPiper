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
from app.models import flatpriceInput,townInput


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html',title='home')

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

@app.route('/resalepriceestimator/<username>',methods=['GET', 'POST'])
@login_required
def resalepriceestimator(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = resalepriceinputform()
    if form.validate_on_submit():
        result = 321321 #PLACEHOLDER, UPDATE WITH MACHINE LEARNING
        rsinput = resaleInput(town=form.town.data,flatType=form.flatType.data, ogprice=form.ogprice.data,
        floorArea=form.floorArea.data, storey=form.storey.data, age=form.age.data, OUTPUT=result, user_id = user.id)
        db.session.add(rsinput)
        db.session.commit()
        return redirect(url_for('resaleprice',username=username,output=result))

    return render_template('resalepriceestimator.html', user=user, form=form)

@app.route('/flatpriceestimator/<username>',methods=['GET', 'POST'])
@login_required
def flatpriceestimator(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = priceEstimatorForm()
    if form.validate_on_submit():
        result=33333 #PLACEHOLDER, UPDATE WITH MACHINE LEARNING
        fpinput = flatpriceInput(town=form.town.data,flatType=form.flatType.data,floorArea=form.floorArea.data,
        storey=form.storey.data, age=form.age.data, OUTPUT=result, user_id = user.id)
        db.session.add(fpinput)
        db.session.commit()
        return redirect(url_for('flatprice',username=username,output=result))
    return render_template('flatpriceestimator.html', user=user, form=form)

@app.route('/townrecommender/<username>',methods=['GET', 'POST'])
@login_required
def townrecommender(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = townForm()
    if form.validate_on_submit():
        result1 = "ANG MO KIO" #PLACEHOLDER, UPDATE WITH MACHINE LEARNING
        result2 = "SENGKANG"
        result3 = "HOUGANG"
        tinput = townInput(flatType=form.flatType.data,floorArea=form.floorArea.data,
        storey=form.storey.data, age=form.age.data, OUTPUT1=result1,OUTPUT2=result2,OUTPUT3=result3, user_id = user.id)
        db.session.add(tinput)
        db.session.commit()
        return redirect(url_for('recommend',username=username,output1=result1,output2=result2,output3=result3))
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
def flatprice(username,output):
    user = User.query.filter_by(username=username).first_or_404()
    output=output
    return render_template('flatprice.html', user=user,output=output)

@app.route('/recommend/<username>/<output1>/<output2>/<output3>')
@login_required
def recommend(username,output1,output2,output3):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('recommend.html', user=user,output1=output1,output2=output2,output3=output3)

@app.route('/resaleprice/<username>/<output>')
@login_required
def resaleprice(username,output):
    user = User.query.filter_by(username=username).first_or_404()
    output=output
    return render_template('resale.html', user=user, output=output)
