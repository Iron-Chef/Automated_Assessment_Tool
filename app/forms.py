from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import Multiplechoice


class LoginForm(FlaskForm):
    username = StringField('Your ID number', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign in')

class QuestionForm(FlaskForm):
    question=StringField(validators=[DataRequired(message="Question is required")])
    answer1=StringField (validators=[DataRequired(message="Minimum of two answer choices are required")])
    ans_multi_select_1 = BooleanField("Option 1")
    answer2=StringField(validators=[DataRequired(message="Minimum of two answer choices are required")])
    ans_multi_select_2 = BooleanField("Option 2")
    answer3=StringField(FlaskForm)
    ans_multi_select_3 = BooleanField("Option 3")
    answer4=StringField(FlaskForm)
    ans_multi_select_4 = BooleanField("Option 4")

    marks=IntegerField(validators=[DataRequired(message="Please enter mark")]) 
    feedback=StringField("Feedback:")
    submit = SubmitField("Form Complete")

def MC_query():
    return Multiplechoice.query

class MCChoiceForm(FlaskForm):
    question_1 = QuerySelectField(query_factory=MC_query, allow_blank=True, get_label='question')
    question_2 = QuerySelectField(query_factory=MC_query, allow_blank=True, get_label='question')
    question_3 = QuerySelectField(query_factory=MC_query, allow_blank=True, get_label='question')
    question_4 = QuerySelectField(query_factory=MC_query, allow_blank=True, get_label='question')
    question_5 = QuerySelectField(query_factory=MC_query, allow_blank=True, get_label='question')