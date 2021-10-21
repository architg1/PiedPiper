from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class priceEstimatorForm(FlaskForm):
    """
    Summary of class:

    Declares a priceEstimatorInputForm which requires the
    user to input their desired flat details.
    
    Required user input:
    1. town
    2. flatType
    3. floor area 
    4. storey
    5. age of flat.
    Lastly a submit field named submit
     
    """
    town = SelectField(u'Select Town', choices=[('ANG MO KIO', 'ANG MO KIO'), ('BEDOK', 'BEDOK'),
                                                ('BISHAN', 'BISHAN'), ('BUKIT BATOK',
                                                                       'BUKIT BATOK'), ('BUKIT MERAH', 'BUKIT MERAH'),
                                                ('BUKIT PANJANG', 'BUKIT PANJANG'), ('BUKIT TIMAH',
                                                                                     'BUKIT TIMAH'), ('CENTRAL AREA', 'CENTRAL AREA'),
                                                ('CHOA CHU KANG', 'CHOA CHU KANG'), ('CLEMENTI', 'CLEMENTI'), (
                                                    'GEYLANG', 'GEYLANG'), ('HOUGANG', 'HOUGANG'),
                                                ('JURONG EAST', 'JURONG EAST'), ('JURONG WEST',
                                                                                 'JURONG WEST'), ('KALLANG/WHAMPOA', 'KALLANG/WHAMPOA'),
                                                ('MARINE PARADE', 'MARINE PARADE'), ('PASIR RIS',
                                                                                     'PASIR RIS'), ('PUNGGOL', 'PUNGGOL'), ('QUEENSTOWN', 'QUEENSTOWN'),
                                                ('SEMBAWANG', 'SEMBAWANG'), ('SENGKANG',
                                                                             'SENGKANG'), ('SERANGOON', 'SERANGOON'), ('TAMPINES', 'TAMPINES'),
                                                ('TOA PAYAH', 'TOA PAYOH'), ('WOODLANDS', 'WOODLANDS'), ('YISHUN', 'YISHUN')])
    flatType = SelectField(u'Select Flat type', choices=[('2 ROOM', '2 ROOM'), (
        '3 ROOM', '3 ROOM'), ('4 ROOM', '4 ROOM'), ('5 ROOM', '5 ROOM'), ('EXECUTIVE', 'EXECUTIVE')])
    floorArea = IntegerField('Enter Floor Area (in sqm)')
    storey = SelectField(u'Select Preferred Storey', choices=[
                         ('01 TO 03', '01 TO 03'), ('04 TO 06', '04 TO 06'), ('07 TO 09', '07 TO 09'),('10 TO 12','10 TO 12'),
                         ('13 TO 15','13 TO 15'),('16 TO 18', '16 TO 18'),('19 TO 21', '19 TO 21'),('22 TO 24','22 TO 24'),
                         ('25 TO 27','25 TO 27'),('28 TO 30','28 TO 30'),('31 TO 33','31 TO 33'),('34 TO 36','34 TO 36'),('37 TO 39','37 TO 39'),
                         ('40 TO 42','40 TO 42'),('43 TO 45','43 TO 45')])
    age = IntegerField(u'Enter expected remaining years of desired flat')
    submit = SubmitField('Submit')