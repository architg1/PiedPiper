from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    ##email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    resaleInput = db.relationship(
        'resaleInput', backref='author', lazy='dynamic')
    flatpriceInput = db.relationship(
        'flatpriceInput', backref='author', lazy='dynamic')
    townInput = db.relationship('townInput', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class resaleInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String(64))
    flatType = db.Column(db.String(64))
    ogprice = db.Column(db.Integer)
    floorArea = db.Column(db.Integer)
    storey = db.Column(db.String(64))
    age = db.Column(db.Integer)
    OUTPUT = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class flatpriceInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String(64))
    flatType = db.Column(db.String(64))
    floorArea = db.Column(db.Integer)
    storey = db.Column(db.String(64))
    age = db.Column(db.Integer)
    OUTPUT = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class townInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flatType = db.Column(db.String(64))
    floorArea = db.Column(db.Integer)
    storey = db.Column(db.String(64))
    age = db.Column(db.Integer)
    OUTPUT1 = db.Column(db.String(64))
    OUTPUT2 = db.Column(db.String(64))
    OUTPUT3 = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
