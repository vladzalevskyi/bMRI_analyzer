from flask_wtf import FlaskForm as Form

from wtforms import PasswordField, StringField, SubmitField, BooleanField, SelectField, IntegerField, FileField, DateTimeField, HiddenField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange, InputRequired
from flask_wtf.file import FileAllowed, FileRequired
from app.db_classes import Therapists, Patients
from  datetime import datetime
class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=19)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=19)])
    remember_me = BooleanField("Remember me")
    submit = SubmitField('Log In')

class SignUpForm(Form):
    title = SelectField(u'Select your title at the hospital', choices=[('nrs', 'nurse'), ('dr', 'Dr.')])
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=20)])
    password2 = PasswordField('Repeat the password', validators=[DataRequired(), Length(max=19), EqualTo('password')])

    fname = StringField("First Name", validators=[DataRequired(), Length(max=20)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Therapists.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class AddPatientForm(Form):
    fname = StringField("First Name", validators=[DataRequired(), Length(max=20)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(max=20)])

    ssn = StringField("SSN", validators=[Length(max=9)])
    gender = SelectField("Patient's gender", choices=[("f", "female"), ("m", "male")])
    age = IntegerField("Patient's age")
    #therapist_id = SelectField(u'Select therapist', coerce=int, validators=[InputRequired()])

    submit = SubmitField('Submit')

    # When you add any methods that match the pattern validate_<field_name>,
    # WTForms takes those as custom validators
    # and invokes them in addition to the stock validators.
    def validate_ssn(self, ssn):
        user = Patients.query.filter_by(ssn=ssn.data).first()
        if user is not None:
            raise ValidationError('Error adding new patient. Check that patient with current ssn already doesn\'t exists')


class ImageForm(Form):
    photo = FileField(label="Select image", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    patient_id = SelectField(u'Select patient', coerce=int, validators=[InputRequired()])
    datetime = DateTimeField("Select datetime of uplodaded image. Default is now()", default=datetime.today)
    im_type = SelectField(u'Select image type', coerce=int, validators=[InputRequired()])
    analyze = BooleanField("Send to analysis module")
    submit = SubmitField('Upload')


class PatientsForm(Form):
    # add validaion fields to be careful
    # quering data and puting it to url
    search_field = StringField('Search for Patients', render_kw={"placeholder": "'Name Surname' OR SSN ('123456789')"})
    sort_by_ssn = BooleanField("using ssn", default=False)
    submit = SubmitField('Search')

class EditImgAnalysisForm(Form):
    img_id = HiddenField("Image id")
    tumor = StringField("Tumor analysis:")
    diagnosis = SelectField(u'Diagnosis', coerce=int, validators=[InputRequired()])
    recommendations = StringField("Recommendations")
    confidence = FloatField("Confidence")
    verified = BooleanField("Verified", default=True)

    submit = SubmitField('Save changes')
