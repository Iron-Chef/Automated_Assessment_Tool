from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Your ID number', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign in')

class CreateTestForm(FlaskForm):
    test_type= BooleanField('Test Type', validators=[DataRequired()])
    submit= SubmitField('Create Test')