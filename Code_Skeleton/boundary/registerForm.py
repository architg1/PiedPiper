from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    """
    Summary of class:

    Declares a RegistrationForm class with required user input attributes username, password, password2
    and a submit field named submit
     
    """
    username = StringField('Username', validators=[DataRequired()])
    ##email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    