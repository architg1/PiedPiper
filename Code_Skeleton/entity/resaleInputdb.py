from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class resaleInput(db.Model):
    """
    Summary of class:

    Database of the history of inputs keyed in resale price estimator for each user
    Attributes:
        1. town
        2. flatType
        3. original price
        4. floor area
        5. storey
        6. age
        7. user id 
        8. OUTPUT which is the result of the predictor
    """
    id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String(64))
    flatType = db.Column(db.String(64))
    ogprice = db.Column(db.Integer)
    floorArea = db.Column(db.Integer)
    storey = db.Column(db.String(64))
    age = db.Column(db.Integer)
    OUTPUT = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))