from flask_wtf import FlaskForm as Form
from wtforms import PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=19)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=19)])
    submit = SubmitField('Submit')

class SignUpForm(Form):
    title = SelectField(u'Select your title at the hospital', choices=[('nrs', 'nurse'), ('dr', 'Dr.')])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=19)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=19)])

    fname = StringField("First Name", validators=[DataRequired(), Length(max=20)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(max=20)])

    submit = SubmitField('Submit')
