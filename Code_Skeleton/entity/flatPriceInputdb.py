from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class flatpriceInput(db.Model):
    """
    Summary of class:

    Database of the history of inputs keyed in flat price estimator for each user
    Attributes:
        1. town
        2. flatType
        3. floor area
        4. storey
        5. age
        6. user id
        7. OUTPUT which is the result of the predictor
    """
    id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String(64))
    flatType = db.Column(db.String(64))
    floorArea = db.Column(db.Integer)
    storey = db.Column(db.String(64))
    age = db.Column(db.Integer)
    OUTPUT = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))