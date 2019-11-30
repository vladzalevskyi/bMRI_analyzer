from flask_wtf import FlaskForm as Form

from wtforms import PasswordField, StringField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange, InputRequired
from app.db_classes import Therapists, Patients
class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=19)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=19)])
    remember_me = BooleanField("Remember me")
    submit = SubmitField('Submit')

class SignUpForm(Form):
    title = SelectField(u'Select your title at the hospital', choices=[('nrs', 'nurse'), ('dr', 'Dr.')])
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=20)])
    password2 = PasswordField('Repeat the password', validators=[DataRequired(), Length(max=19), EqualTo('password')])

    fname = StringField("First Name", validators=[DataRequired(), Length(max=20)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = Therapists.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class AddPatientForm(Form):
    fname = StringField("First Name", validators=[DataRequired(), Length(max=20)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(max=20)])

    ssn = StringField("SSN", validators=[Length(min=9, max=9)])
    gender = SelectField("Patient's gender", choices=[("f", "female"), ("m", "male")])
    age = IntegerField("Patient's age", validators=[NumberRange(min=0, max=200)])
    therapist_id = SelectField(u'Select therapist', coerce=int, validators=[InputRequired()])

    submit = SubmitField('Submit')

    # When you add any methods that match the pattern validate_<field_name>, 
    # WTForms takes those as custom validators 
    # and invokes them in addition to the stock validators.
    def validate_ssn(self, ssn):
        user = Patients.query.filter_by(ssn=ssn.data).first()
        if user is not None:
            raise ValidationError('Patient with current ssn already exists')
