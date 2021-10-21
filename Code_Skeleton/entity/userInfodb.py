from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    """
    Summary of class:

    Database of user information
    Attributes:
        1. username
        2. password in hash
        3. resale price input history
        4. flat price estimator input history
        5. town estimator input history  
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    ##email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ##posts = db.relationship('Post', backref='author', lazy='dynamic')
    resaleInput = db.relationship(
        'resaleInput', backref='author', lazy='dynamic')
    flatpriceInput = db.relationship(
        'flatpriceInput', backref='author', lazy='dynamic')
    townInput = db.relationship('townInput', backref='author', lazy='dynamic')

   

    def __repr__(self):
        return '<User {}>'.format(self.username)