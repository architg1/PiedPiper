from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class townForm(FlaskForm):
    """
    Summary of class:

    Declares a townForm which requires the
    user to input their desired flat details.
    
    Required user input:
    1. budget
    2. flatType
    3. floor area 
    4. storey
    5. age of flat
    Lastly a submit field named submit
     
    """
    flatType = SelectField(u'Select Flat type', choices=[('2 ROOM', '2 ROOM'), (
        '3 ROOM', '3 ROOM'), ('4 ROOM', '4 ROOM'), ('5 ROOM', '5 ROOM'), ('EXECUTIVE', 'EXECUTIVE')])
    floorArea = IntegerField('Enter Floor Area (in sqm)')
    storey = SelectField(u'Select Preferred Storey', choices=[
                         ('01 TO 03', '01 TO 03'), ('04 TO 06', '04 TO 06'), ('07 TO 09', '07 TO 09'),('10 TO 12','10 TO 12'),
                         ('13 TO 15','13 TO 15'),('16 TO 18', '16 TO 18'),('19 TO 21', '19 TO 21'),('22 TO 24','22 TO 24'),
                         ('25 TO 27','25 TO 27'),('28 TO 30','28 TO 30'),('31 TO 33','31 TO 33'),('34 TO 36','34 TO 36'),('37 TO 39','37 TO 39'),
                         ('40 TO 42','40 TO 42'),('43 TO 45','43 TO 45')])
    age = IntegerField(u'Enter expected remaining years of desired flat')
    budget = IntegerField(u'Enter expected budget in SGD')
    submit = SubmitField('Submit')