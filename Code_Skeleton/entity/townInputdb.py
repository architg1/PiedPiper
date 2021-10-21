from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class townInput(db.Model):
    """
    Summary of class:

    Database of the history of inputs keyed in town predictor for each user
    Attributes:
        1. Budget
        2. flatType
        3. floor area
        4. storey
        5. age
        6. OUTPUT which is the result of the predictor
        7. user id
    """
    id = db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.Integer)
    flatType = db.Column(db.String(64))
    floorArea = db.Column(db.Integer)
    storey = db.Column(db.String(64))
    age = db.Column(db.Integer)
    OUTPUT = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))