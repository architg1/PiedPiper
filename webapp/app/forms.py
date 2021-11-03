from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    ##email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class resalepriceinputform(FlaskForm):
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
    ogprice = IntegerField('Enter Original Price')
    floorArea = IntegerField('Enter Floor Area (in sqm)')
    storey = SelectField(u'Select Storey of Flat', choices=[
                         ('01 TO 03', '01 TO 03'), ('04 TO 06', '04 TO 06'), ('07 TO 09',
                                                                              '07 TO 09'), ('10 TO 12', '10 TO 12'),
                         ('13 TO 15', '13 TO 15'), ('16 TO 18', '16 TO 18'), ('19 TO 21',
                                                                              '19 TO 21'), ('22 TO 24', '22 TO 24'),
                         ('25 TO 27', '25 TO 27'), ('28 TO 30', '28 TO 30'), ('31 TO 33',
                                                                              '31 TO 33'), ('34 TO 36', '34 TO 36'), ('37 TO 39', '37 TO 39'),
                         ('40 TO 42', '40 TO 42'), ('43 TO 45', '43 TO 45')])
    age = IntegerField(u'Enter remaining years of flat')
    submit = SubmitField('Submit')


class priceEstimatorForm(FlaskForm):
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
                         ('01 TO 03', '01 TO 03'), ('04 TO 06', '04 TO 06'), ('07 TO 09',
                                                                              '07 TO 09'), ('10 TO 12', '10 TO 12'),
                         ('13 TO 15', '13 TO 15'), ('16 TO 18', '16 TO 18'), ('19 TO 21',
                                                                              '19 TO 21'), ('22 TO 24', '22 TO 24'),
                         ('25 TO 27', '25 TO 27'), ('28 TO 30', '28 TO 30'), ('31 TO 33',
                                                                              '31 TO 33'), ('34 TO 36', '34 TO 36'), ('37 TO 39', '37 TO 39'),
                         ('40 TO 42', '40 TO 42'), ('43 TO 45', '43 TO 45')])
    age = IntegerField(u'Enter expected remaining years of desired flat')
    submit = SubmitField('Submit')


class townForm(FlaskForm):
    flatType = SelectField(u'Select Flat type', choices=[('2 ROOM', '2 ROOM'), (
        '3 ROOM', '3 ROOM'), ('4 ROOM', '4 ROOM'), ('5 ROOM', '5 ROOM'), ('EXECUTIVE', 'EXECUTIVE')])
    floorArea = IntegerField('Enter Floor Area (in sqm)')
    storey = SelectField(u'Select Preferred Storey', choices=[
                         ('01 TO 03', '01 TO 03'), ('04 TO 06', '04 TO 06'), ('07 TO 09',
                                                                              '07 TO 09'), ('10 TO 12', '10 TO 12'),
                         ('13 TO 15', '13 TO 15'), ('16 TO 18', '16 TO 18'), ('19 TO 21',
                                                                              '19 TO 21'), ('22 TO 24', '22 TO 24'),
                         ('25 TO 27', '25 TO 27'), ('28 TO 30', '28 TO 30'), ('31 TO 33',
                                                                              '31 TO 33'), ('34 TO 36', '34 TO 36'), ('37 TO 39', '37 TO 39'),
                         ('40 TO 42', '40 TO 42'), ('43 TO 45', '43 TO 45')])
    age = IntegerField(u'Enter expected remaining years of desired flat')
    budget = IntegerField(u'Enter expected budget in SGD')
    submit = SubmitField('Submit')
