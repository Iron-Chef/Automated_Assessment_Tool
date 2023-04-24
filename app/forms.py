from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, RadioField, FormField, validators
from wtforms.validators import DataRequired, Optional, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.widgets import TextArea
from app.models import Multiplechoice


class LoginForm(FlaskForm):
    username = StringField('Your ID number', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign in')

DIFFICULTY_RATING =[(0,u' '), (5,u'★★★★★'), (4,u'★★★★'),(3,u'★★★'),(2,'★★'),(1,u'★')]

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
    subject = RadioField("Subject: ", choices = [
        ("Java", "Java"),
        ("JavaScript", "JavaScript"),
        ("Python", "Python"),
        ("SQL", "SQL"),
        ("Other", "Other"),
        ],
        coerce = str, validators = [DataRequired()])
    topic = StringField(validators = [DataRequired (message = "Please enter the topic of the question: ")])
    marks=IntegerField(validators=[DataRequired(message="Please enter mark"),NumberRange(min=1)]) 
    feedback=StringField("Feedback:")
    submit = SubmitField("Add Question")

#allows mc questions to be written when creating formative test - RJ
class QuestionFormFormField(FlaskForm):
    question=StringField("question",[validators.Optional()])
    answer1=StringField ("answer 1",[validators.Optional()])
    ans_multi_select_1 = BooleanField("is this the correct answer?",[validators.Optional()])
    answer2=StringField("answer 2",[validators.Optional()])
    ans_multi_select_2 = BooleanField("is this the correct answer?",[validators.Optional()])
    answer3=StringField("answer 3",[validators.Optional()])
    ans_multi_select_3 = BooleanField("is this the correct answer?",[validators.Optional()])
    answer4=StringField("answer 4",[validators.Optional()])
    ans_multi_select_4 = BooleanField("is this the correct answer?",[validators.Optional()])
    rating = SelectField('Rating:',choices=DIFFICULTY_RATING, coerce=int, validators = [validators.Optional()])
    subject = RadioField("Subject: ", choices = [
        ("Java", "Java"),
        ("JavaScript", "JavaScript"),
        ("Python", "Python"),
        ("SQL", "SQL"),
        ("Other", "Other"),
        ],
        coerce = str, validators = [validators.Optional()])
    topic = StringField("topic",[validators.Optional()])
    marks=IntegerField("marks",[validators.Optional()]) 
    feedback=StringField("Feedback:",[validators.Optional()])

#allows fill in the gap questions to be written when filling in the gap - rj 
class FillInTheBlankQuestionFormFormField(FlaskForm):
    question = StringField("Question: ", [validators.Optional()])
    answer = StringField("Answer: ", [validators.Optional()])
    subject = RadioField("Subject: ", 
        choices = [
        ("Java", "Java"),
        ("JavaScript", "JavaScript"),
        ("Python", "Python"),
        ("SQL", "SQL"),
        ("Other", "Other"),
        ],
        coerce = str, 
        validators = [validators.Optional()])
    marks=IntegerField("marks",[validators.Optional()])
    rating = SelectField('Rating:',choices=DIFFICULTY_RATING, coerce=int, validators = [validators.Optional()])
    feedback=StringField("Feedback:",[validators.Optional()])
    topic = StringField("topic",[validators.Optional()])

#to choose which path to go down Sum/form - RJ
class TestChoice(FlaskForm):
    question_module = SelectField('module', choices=[])
    test_type = SelectField('Test Type', choices=['Summative', 'Formative'])
    test_title = StringField('Test Title')

#this is needed for queryselectfield to work - RJ
def Q_query():
    return Multiplechoice.query

#form for create formative test page - RJ
class QChoiceForm(FlaskForm):
    question_1 = QuerySelectField(query_factory=Q_query, allow_blank=False, get_label='question')
    WriteMCquestion_1 = FormField(QuestionFormFormField)
    WriteFTGquestion_1 = FormField(FillInTheBlankQuestionFormFormField)
    question_2 = QuerySelectField(query_factory=Q_query, allow_blank=False, get_label='question')
    WriteMCquestion_2 = FormField(QuestionFormFormField)
    WriteFTGquestion_2 = FormField(FillInTheBlankQuestionFormFormField)
    question_3 = QuerySelectField(query_factory=Q_query, allow_blank=False, get_label='question')
    WriteMCquestion_3 = FormField(QuestionFormFormField)
    WriteFTGquestion_3 = FormField(FillInTheBlankQuestionFormFormField)
    question_4 = QuerySelectField(query_factory=Q_query, allow_blank=False, get_label='question')
    WriteMCquestion_4 = FormField(QuestionFormFormField)
    WriteFTGquestion_4 = FormField(FillInTheBlankQuestionFormFormField)
    question_5 = QuerySelectField(query_factory=Q_query, allow_blank=False, get_label='question')
    WriteMCquestion_5 = FormField(QuestionFormFormField)
    WriteFTGquestion_5 = FormField(FillInTheBlankQuestionFormFormField)
    Test_feedback=StringField("Test Feedback:")

class EmptyForm(FlaskForm):
  submit = SubmitField('Submit')

class TakeFormTestForm(FlaskForm):
    ready = BooleanField("Yes")
    submitS = SubmitField("Start test")

class Q1TakeFormTestForm(FlaskForm):
    q1_ans_multi_select_1 = BooleanField("Option 1")
    q1_ans_multi_select_2 = BooleanField("Option 2")
    q1_ans_multi_select_3 = BooleanField("Option 3")
    q1_ans_multi_select_4 = BooleanField("Option 4")
    q1_ans_FTG = StringField("Type answer")
    q1_submit = SubmitField("q1 check answer")

class Q2TakeFormTestForm(FlaskForm):   
    q2_ans_multi_select_1 = BooleanField("Option 1")
    q2_ans_multi_select_2 = BooleanField("Option 2")
    q2_ans_multi_select_3 = BooleanField("Option 3")
    q2_ans_multi_select_4 = BooleanField("Option 4")
    q2_ans_FTG = StringField("Type answer")
    q2_submit = SubmitField("q2 check answer")

class Q3TakeFormTestForm(FlaskForm):
    q3_ans_multi_select_1 = BooleanField("Option 1")
    q3_ans_multi_select_2 = BooleanField("Option 2")
    q3_ans_multi_select_3 = BooleanField("Option 3")
    q3_ans_multi_select_4 = BooleanField("Option 4")
    q3_ans_FTG = StringField("Type answer")
    q3_submit = SubmitField("q3 check answer")

class Q4TakeFormTestForm(FlaskForm):
    q4_ans_multi_select_1 = BooleanField("Option 1")
    q4_ans_multi_select_2 = BooleanField("Option 2")
    q4_ans_multi_select_3 = BooleanField("Option 3")
    q4_ans_multi_select_4 = BooleanField("Option 4")
    q4_ans_FTG = StringField("Type answer")
    q4_submit = SubmitField("q4 check answer")

class Q5TakeFormTestForm(FlaskForm):
    q5_ans_multi_select_1 = BooleanField("Option 1")
    q5_ans_multi_select_2 = BooleanField("Option 2")
    q5_ans_multi_select_3 = BooleanField("Option 3")
    q5_ans_multi_select_4 = BooleanField("Option 4")
    q5_ans_FTG = StringField("Type answer")
    q5_submit = SubmitField("q5 check answer")

class FinishFormTestForm(FlaskForm):
    finished = BooleanField("Yes")
    submitF = SubmitField('Finish')

class StudentAnswerForm(FlaskForm):
    ans_multi_select_1 = BooleanField("Option 1")
    ans_multi_select_2 = BooleanField("Option 2")
    ans_multi_select_3 = BooleanField("Option 3")
    ans_multi_select_4 = BooleanField("Option 4")
    ans_FTG = StringField("Type answer")
    subject = RadioField("Subject: ", choices = [
        ("Java", "Java"),
        ("JavaScript", "JavaScript"),
        ("Python", "Python"),
        ("SQL", "SQL"),
        ("Other", "Other"),
        ],
        coerce = str, validators = [DataRequired()])
    marks = IntegerField(validators=[DataRequired(message="Please enter mark")]) 
    feedback = StringField("Feedback:")
    topic = StringField("Topic: ")
    submit = SubmitField("Done")

class FillInTheBlankQuestionForm(FlaskForm):
    question = StringField("Question: ", validators = [DataRequired (message = "Please type a question.")])
    answer = StringField("Answer: ", validators = [DataRequired (message = "Please provide an answer.")])
    subject = RadioField("Subject: ", 
        choices = [
        ("Java", "Java"),
        ("JavaScript", "JavaScript"),
        ("Python", "Python"),
        ("SQL", "SQL"),
        ("Other", "Other"),
        ],
        coerce = str, 
        validators = [DataRequired (message = "Please select a subject.")])
    marks = IntegerField(validators = [DataRequired (message = "Please enter a mark.")])
    rating = SelectField("Difficulty Rating:", choices = DIFFICULTY_RATING, coerce=int)
    feedback = StringField ("Feedback: ")
    topic = StringField("Topic: ")
    submit = SubmitField("Done")

class CreateTestForm(FlaskForm):
    test_type= SelectField('Check to make test summative',choices=[(0,"formative"),(1,"summative")])
    title=StringField('Title of test')
    rating=SelectField('Rate the test', choices=[(1,"Easy"),(2,"Medium-Easy"),(3,"Medium"),(4,"Medium-Hard"),(5,"Hard")])
    module=SelectField('Module Integer', choices=[])
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
    marks=IntegerField('score')
    submit= SubmitField('Submit Test Attempt')

class ResultsForm(FlaskForm):
    attempt_id=IntegerField('attempt_id')
    marks=IntegerField('marks')

