from flask_wtf import FlaskForm as Form

from wtforms import PasswordField, StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.db_classes import Therapists
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
    password2 = PasswordField('Password', validators=[DataRequired(), Length(max=19), EqualTo('password')])

    fname = StringField("First Name", validators=[DataRequired(), Length(max=20)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = Therapists.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')