from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField,SelectField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    username = StringField('Your ID number', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign in')

DIFFICULTY_RATING =[(5,u'★★★★★'), (4,u'★★★★'),(3,u'★★★'),(2,'★★'),(1,u'★')]

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
    rating = SelectField('Rating:',choices=DIFFICULTY_RATING, coerce=int)
    marks=IntegerField(validators=[DataRequired(message="Please enter mark")]) 
    feedback=StringField("Feedback:")
    submit = SubmitField("Add Question")

class CreateTestForm(FlaskForm):
    test_type= SelectField('Check to make test summative',choices=[(0,"formative"),(1,"summative")])
    question_id_1=SelectField('question',choices=[])
    question_id_2=SelectField('question',choices=[])
    question_id_3=SelectField('question',choices=[])
    question_id_4=SelectField('question',choices=[])
    question_id_5=SelectField('question',choices=[])
    submit= SubmitField('Create Test')

class SubmitAttemptForm(FlaskForm):
    answer_1=SelectField('question',choices=[])
    answer_2=SelectField('question',choices=[])
    answer_3=SelectField('question',choices=[])
    answer_4=SelectField('question',choices=[])
    answer_5=SelectField('question',choices=[])
    answer_1_correct=IntegerField('correct')
    answer_2_correct=IntegerField('correct')
    answer_3_correct=IntegerField('correct')
    answer_4_correct=IntegerField('correct')
    answer_5_correct=IntegerField('correct')
    score=IntegerField('score')
    submit= SubmitField('Submit Test Attempt')
