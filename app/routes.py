import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as opy
from plotly.subplots import make_subplots
from collections import Counter
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy import *
from datetime import datetime
import random
from app.functions import *
from app.models import User,Test, Multiplechoice, Results_sum, Module, Studentanswer, Formativetest
from app.forms import DIFFICULTY_RATING, LoginForm, CreateTestForm, QuestionForm, SubmitAttemptForm, StudentAnswerForm, ResultsForm, FillInTheBlankQuestionForm, QChoiceForm, TestChoice, TakeFormTestForm, Q1TakeFormTestForm, Q2TakeFormTestForm, Q3TakeFormTestForm, Q4TakeFormTestForm, Q5TakeFormTestForm, FinishFormTestForm
from app import app,db
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np


@app.route('/login', methods = ['GET', 'POST'])
def login():

    form = LoginForm()

    if current_user.is_authenticated:
        
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user)

        # This is a cybersecurity feature
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(url_for('index'))

    return render_template('login.html', title = 'Login', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = User.query.all()
    return render_template('index.html',user=user, title = 'Home')

@app.route("/create_test",methods=['GET','POST'])
@login_required
def create_test():
  form = CreateTestForm() 
  questions=Multiplechoice.query.all()
  modules=Module.query.all()
  form.module.choices=[(module.id,module.name) for module in modules]
  form.rating.choices=[(question.rating_num,question.rating_num) for question in questions]
  form.question_id_1.choices = [(question.id,question.id) for question in questions]
  form.question_id_2.choices = [(question.id,question.id) for question in questions]
  form.question_id_3.choices = [(question.id,question.id) for question in questions]
  form.question_id_4.choices = [(question.id,question.id) for question in questions]
  form.question_id_5.choices = [(question.id,question.id) for question in questions]
  rating=0
  if form.validate_on_submit():
    test=Test(test_type=form.test_type.data,creator_id=current_user.id,question_id_1=form.question_id_1.data,question_id_2=form.question_id_2.data,question_id_3=form.question_id_3.data,question_id_4=form.question_id_4.data,question_id_5=form.question_id_5.data, module=form.module.data, title=form.title.data, rating=form.rating.data)
    db.session.add(test)
    db.session.commit()
    flash('Test Creation Succesful!')
    return redirect(url_for('index'))
  return render_template('create_test.html',title='Create Test',form=form,questions=questions, modules=modules)

# Add multiple choice questions
@app.route('/add_mc_questions', methods=['GET', 'POST'])
@login_required
def add_mc_question():
    form=QuestionForm()
    
    if form.validate_on_submit():
        multi= Multiplechoice(
        user_id=current_user.id,
        question=form.question.data, 
        answer_1=form.answer1.data,
        ans_choice_1=form.ans_multi_select_1.data, 
        answer_2=form.answer2.data,
        ans_choice_2=form.ans_multi_select_2.data, 
        answer_3=form.answer3.data, 
        ans_choice_3=form.ans_multi_select_3.data,
        answer_4=form.answer4.data, 
        ans_choice_4=form.ans_multi_select_4.data,
        subject_tag = form.subject.data,
        marks=form.marks.data, 
        rating = dict(DIFFICULTY_RATING).get(form.rating.data),
        rating_num= form.rating.data,
        feedback=form.feedback.data,
        topic_tag = form.topic.data,
        question_type = "multiple_choice"
        )
        if multi.ans_choice_1 + multi.ans_choice_2 + multi.ans_choice_3 + multi.ans_choice_4 == 1:
            db.session.add(multi)
        
            db.session.commit()
            flash("Question added")
            return redirect('/question_list')
        else:
            flash("Choose one answer choice")
        db.session.commit()
        
    return render_template("add_mc_questions.html", title="Add Multiple Choice Questions", form=form)

#List of MSc Computing Modules
@app.route('/modules', methods=['GET'])
def modules():
    modules = Module.query.all()
    return render_template('modules.html',title='MSc Computing Modules',modules=modules)

#Delete a multiple choice question- may add in warning before
@app.route("/mc_question/delete/<int:mc_question_id>")
@login_required
def delete_mcquestion(mc_question_id):
    mcquestion_to_delete=Multiplechoice.query.get_or_404(mc_question_id)

    try:
        db.session.delete(mcquestion_to_delete)
        db.session.commit()
        flash("Question deleted!")

        return redirect('/question_list')

    except:
        flash("Problem deleting question, please check with Admin!")

        return redirect('/question_list')

#view individual mc question by id
@app.route("/mc_question/<int:mc_question_id>", methods=['GET'])
@login_required
def mcquestion(mc_question_id):
    mcquestion=Multiplechoice.query.get_or_404(mc_question_id)

    return render_template('mc_question.html', mcquestion=mcquestion, title=mcquestion.question, mc_question_id=mcquestion.id)

# edit mc questions
@app.route("/mc_question/edit/<int:mc_question_id>", methods=['GET', 'POST'])
@login_required
def edit_mc_question(mc_question_id):
    mcquestion = Multiplechoice.query.get_or_404(mc_question_id)
    form = QuestionForm()
    if form.validate_on_submit():
        mcquestion.question=form.question.data
        mcquestion.answer_1=form.answer1.data
        mcquestion.ans_choice_1=form.ans_multi_select_1.data
        mcquestion.answer_2=form.answer2.data
        mcquestion.ans_choice_2=form.ans_multi_select_2.data
        mcquestion.answer_3=form.answer3.data
        mcquestion.ans_choice_3=form.ans_multi_select_3.data
        mcquestion.answer_4=form.answer4.data 
        mcquestion.ans_choice_4=form.ans_multi_select_4.data
        mcquestion.marks=form.marks.data
        mcquestion.feedback=form.feedback.data
        mcquestion.rating = dict(DIFFICULTY_RATING).get(form.rating.data)
        mcquestion.rating_num= form.rating.data
        db.session.add(mcquestion)
        if mcquestion.ans_choice_1 + mcquestion.ans_choice_2 + mcquestion.ans_choice_3 + mcquestion.ans_choice_4 == 1:
            db.session.commit()
            flash("Multiple Choice Question amended")
            return redirect('/question_list')
        else:
            flash("Choose one answer choice")

    form.question.data=mcquestion.question
    form.answer1.data=mcquestion.answer_1
    form.ans_multi_select_1.data=mcquestion.ans_choice_1
    form.answer2.data=mcquestion.answer_2
    form.ans_multi_select_2.data=mcquestion.ans_choice_2
    form.answer3.data=mcquestion.answer_3
    form.ans_multi_select_3.data=mcquestion.ans_choice_3
    form.answer4.data=mcquestion.answer_4
    form.ans_multi_select_4.data=mcquestion.ans_choice_4
    form.marks.data=mcquestion.marks
    form.rating.data=mcquestion.rating
    form.feedback.data=mcquestion.feedback
    return render_template('edit_mc_question.html', mcquestion=mcquestion,form=form)

# Add fill-in-the-blank questions directly
@app.route("/add_fill_in_the_blank_question", methods = ['GET', 'POST'])
def add_fill_in_the_blank_question():

    form = FillInTheBlankQuestionForm()

    if form.validate_on_submit():

        question = Multiplechoice(
        user_id = current_user.id,
        question = form.question.data, 
        answer_1 = form.answer.data,
        subject_tag = form.subject.data,
        marks = form.marks.data,
        rating = dict(DIFFICULTY_RATING).get(form.rating.data),
        rating_num = form.rating.data,
        feedback = form.feedback.data,
        topic_tag = form.topic.data,
        question_type = "fill_in_the_blank"
        )
        db.session.add(question)
        db.session.commit()

        flash('Question added!')
        return redirect('/question_list')

    return render_template('add_fill_in_the_blank_question.html', title = "Add Fill-in-the-blank questions", form = form)

# This is to display the above app route, but directly inside creating a test - AC
@app.route("/add_fill_in_the_blank_question_(test_window)", methods = ['GET', 'POST'])
def add_fill_in_the_blank_question_inside_test():

    form = FillInTheBlankQuestionForm()

    if form.validate_on_submit():

        question = Multiplechoice(
        user_id = current_user.id,
        question = form.question.data, 
        answer_1 = form.answer.data,
        subject_tag = form.subject.data,
        marks = form.marks.data,
        rating = dict(DIFFICULTY_RATING).get(form.rating.data),
        rating_num = form.rating.data,
        feedback = form.feedback.data,
        topic_tag = form.topic.data,
        question_type = "fill_in_the_blank"
        )
        db.session.add(question)
        db.session.commit()

        flash('Question added!')
        return redirect('/create_form_test')

    return render_template('add_fill_in_the_blank_question_(test_window).html', form = form)

#view list of questions- opportunity to list by different queries
@app.route("/fill_in_the_blank_question/<int:fill_in_the_blank_question_id>", methods=['GET'])
def fill_in_the_blank_question(fill_in_the_blank_question_id):

    fill_in_the_blank_question = Multiplechoice.query.get_or_404(fill_in_the_blank_question_id)

    return render_template(
        'fill_in_the_blank_question.html',
        fill_in_the_blank_question = fill_in_the_blank_question,
        title = fill_in_the_blank_question.question, 
        fill_in_the_blank_question_id = fill_in_the_blank_question_id
    )

@app.route("/edit_fill_in_the_blank_question/Question_<int:fill_in_the_blank_question_id>", methods=['GET', 'POST'])
def edit_fill_in_the_blank_question(fill_in_the_blank_question_id):

    fill_in_the_blank_question = Multiplechoice.query.get_or_404(fill_in_the_blank_question_id)

    form = FillInTheBlankQuestionForm()

    if form.validate_on_submit():
        fill_in_the_blank_question.question = form.question.data
        fill_in_the_blank_question.answer_1 = form.answer.data
        fill_in_the_blank_question.subject_tag = form.subject.data
        fill_in_the_blank_question.marks = form.marks.data
        fill_in_the_blank_question.rating = dict(DIFFICULTY_RATING).get(form.rating.data)
        fill_in_the_blank_question.rating_num = form.rating.data
        fill_in_the_blank_question.feedback = form.feedback.data 
        fill_in_the_blank_question.topic_tag = form.topic.data

        db.session.add(fill_in_the_blank_question)
        db.session.commit()

        flash("Question amended")
        return redirect('/question_list')

    form.question.data = fill_in_the_blank_question.question
    form.answer.data = fill_in_the_blank_question.answer_1
    form.subject.data = fill_in_the_blank_question.subject_tag
    form.marks.data = fill_in_the_blank_question.marks
    form.rating.data == dict(DIFFICULTY_RATING).get(fill_in_the_blank_question.rating)
    form.feedback.data = fill_in_the_blank_question.feedback
    form.topic.data = fill_in_the_blank_question.topic_tag

    return render_template('edit_fill_in_the_blank_question.html', title = "Edit Question", form = form,fill_in_the_blank_question = fill_in_the_blank_question, fill_in_the_blank_question_id = fill_in_the_blank_question_id)

@app.route("/fill_in_the_blank_question/delete/<int:fill_in_the_blank_question_id>")
def delete_fill_in_the_blank_question(fill_in_the_blank_question_id):

    fill_in_the_blank_question_to_delete = Multiplechoice.query.get_or_404(fill_in_the_blank_question_id)

    try:
        db.session.delete(fill_in_the_blank_question_to_delete)
        db.session.commit()
        flash("Question deleted!")

        return redirect('/question_list')

    except:
        flash(fill_in_the_blank_question_to_delete.question)

        return redirect('/question_list')

@app.route("/question_list/<order_by>", methods = ['GET'])
@app.route("/<order_by>")
def question_list(order_by):
    
    questions = Multiplechoice.query.all()

    if order_by == "question_type":
        questions = Multiplechoice.query.order_by(Multiplechoice.question_type)
    elif order_by == "topic":
        questions = Multiplechoice.query.order_by(Multiplechoice.topic_tag)
    elif order_by == "marks_asc":
        questions = Multiplechoice.query.order_by(Multiplechoice.marks)
    elif order_by == "marks_desc":
        questions = Multiplechoice.query.order_by(Multiplechoice.marks.desc())
    elif order_by == "difficulty_asc":
        questions = Multiplechoice.query.order_by(Multiplechoice.rating_num)
    elif order_by == "difficulty_desc":
        questions = Multiplechoice.query.order_by(Multiplechoice.rating_num.desc())
    
    return render_template('question_list.html', title = "Previous Questions", questions = questions)

#Individual student answer attempt to test funtionality
@app.route("/student_answer/<int:question_id>", methods=['GET', 'POST'])
@login_required
def student_answer(question_id):

    form=StudentAnswerForm()
    mc_question=Multiplechoice.query.get_or_404(question_id)
    answers=Studentanswer.query.all()

    if form.validate_on_submit():
        if request.method == 'POST':
            mc =Studentanswer(
            user_id=current_user.id,
            question_id=mc_question.id, 
            ans_choice_1=form.ans_multi_select_1.data, 
            ans_choice_2=form.ans_multi_select_2.data, 
            ans_choice_3=form.ans_multi_select_3.data,
            ans_choice_4=form.ans_multi_select_4.data,
            
        )
        db.session.add(mc)
        db.session.commit()
        flash('Your answer is submitted!')
        return redirect(url_for('index'))
    return render_template('student_answer.html',mc_question=mc_question, answers=answers, form=form)

#currently working on this-AJ, NOT WORKING
@app.route("/student_answer_result/<int:question_id>", methods=['GET', 'POST'])
@login_required
def student_answer_result(question_id):
    user_id=current_user.id
    mc_question=Multiplechoice.query.get_or_404(question_id)
    answers=Studentanswer.query.all()
    
    return render_template('student_answer_result.html', mc_question=mc_question,answers=answers, user_id=user_id)


@app.route("/test_list",methods=['GET'])
def test_list():
    tests=Test.query.all() 
    return render_template('test_list.html',tests=tests)

#Generate page for individual tests-DD
@app.route("/test/<int:test_id>")
def test(test_id):
  tests=Test.query.get_or_404(test_id)
  question_1 = Multiplechoice.query.filter_by(id=tests.question_id_1).first()
  question_2 = Multiplechoice.query.filter_by(id=tests.question_id_2).first()
  question_3 = Multiplechoice.query.filter_by(id=tests.question_id_3).first()
  question_4 = Multiplechoice.query.filter_by(id=tests.question_id_4).first()
  question_5 = Multiplechoice.query.filter_by(id=tests.question_id_5).first()
  return render_template('test.html',tests=tests,question_1=question_1,question_2=question_2,question_3=question_3,question_4=question_4,question_5=question_5)

## Adapted this from anthonys code above-DD
@app.route("/test/delete/<int:test_id>")
def delete_test(test_id):
    delete_test=Test.query.get_or_404(test_id)

    try:
        db.session.delete (delete_test)
        db.session.commit()
        flash("Test deleted!")

        tests=Test.query.all()
        return redirect('test_list',tests=tests)

    except:
        flash("Problem deleting test, please check with Admin!")

        tests=Test.query.all()
        return render_template('test_list.html',tests=tests)

@app.route("/test/edit/<int:test_id>", methods=['GET', 'POST'])
def edit_test(test_id):
    form=CreateTestForm()
    test=Test.query.get_or_404(test_id)
    questions=Multiplechoice.query.all()
    form.question_id_1.choices = [(question.id,question.id) for question in questions]
    form.question_id_2.choices = [(question.id,question.id) for question in questions]
    form.question_id_3.choices = [(question.id,question.id) for question in questions]
    form.question_id_4.choices = [(question.id,question.id) for question in questions]
    form.question_id_5.choices = [(question.id,question.id) for question in questions]

    if form.validate_on_submit():
        test.test_type=form.test_type.data
        test.question_id_1=form.question_id_1.data
        test.question_id_2=form.question_id_2.data
        test.question_id_3=form.question_id_3.data
        test.question_id_4=form.question_id_4.data
        test.question_id_5=form.question_id_5.data
        db.session.add(test)
        db.session.commit()
        flash("Test amended")
        return redirect('/test_list')

    form.test_type.data=test.test_type
    form.question_id_1.data=test.question_id_1
    form.question_id_2.data=test.question_id_2
    form.question_id_3.data=test.question_id_3
    form.question_id_4.data=test.question_id_4
    form.question_id_5.data=test.question_id_5
    return render_template('edit_test.html', test=test,form=form,questions=questions)

@app.route("/attempt_test/<int:test_id>",methods=['GET','POST'])
@login_required
def attempt_test(test_id):
  form = SubmitAttemptForm()
  test=Test.query.get_or_404(test_id)
  question_1 = Multiplechoice.query.filter_by(id=test.question_id_1).first()
  question_2 = Multiplechoice.query.filter_by(id=test.question_id_2).first()
  question_3 = Multiplechoice.query.filter_by(id=test.question_id_3).first()
  question_4 = Multiplechoice.query.filter_by(id=test.question_id_4).first()
  question_5 = Multiplechoice.query.filter_by(id=test.question_id_5).first()
  form.answer_1.choices = [(question_1.ans_choice_1,question_1.answer_1),(question_1.ans_choice_2,question_1.answer_2),(question_1.ans_choice_3,question_1.answer_3),(question_1.ans_choice_4,question_1.answer_4)]
  form.answer_2.choices = [(question_2.ans_choice_1,question_2.answer_1),(question_2.ans_choice_2,question_2.answer_2),(question_2.ans_choice_3,question_2.answer_3),(question_2.ans_choice_4,question_2.answer_4)]
  form.answer_3.choices = [(question_3.ans_choice_1,question_3.answer_1),(question_3.ans_choice_2,question_3.answer_2),(question_3.ans_choice_3,question_3.answer_3),(question_3.ans_choice_4,question_3.answer_4)]
  form.answer_4.choices = [(question_4.ans_choice_1,question_4.answer_1),(question_4.ans_choice_2,question_4.answer_2),(question_4.ans_choice_3,question_4.answer_3),(question_4.ans_choice_4,question_4.answer_4)]
  form.answer_5.choices = [(question_5.ans_choice_1,question_5.answer_1),(question_5.ans_choice_2,question_5.answer_2),(question_5.ans_choice_3,question_5.answer_3),(question_5.ans_choice_4,question_5.answer_4)]
  module= Module.query.filter_by(id=test.module).first()
  marks=0
  q1_mark=0
  q1_attempts=1
  q2_mark=0
  q2_attempts=1
  q3_mark=0
  q3_attempts=1
  q4_mark=0
  q4_attempts=1
  q5_mark=0
  q5_attempts=1
  weight=question_1.marks+question_2.marks+question_3.marks+question_4.marks+question_5.marks

  if form.validate_on_submit():
    if form.answer_1.data =="1":
        marks+=question_1.marks
        q1_mark+=question_1.marks
    if form.answer_2.data =="1":
        marks+=question_2.marks
        q2_mark+=question_2.marks
    if form.answer_3.data =="1":
        marks+=question_3.marks
        q3_mark+=question_3.marks
    if form.answer_4.data =="1":
        marks+=question_4.marks
        q4_mark+=question_4.marks
    if form.answer_5.data =="1":
        marks+=question_5.marks
        q5_mark+=question_5.marks
    result_sum=Results_sum(test_id=test.test_id,
    user_id=current_user.id,
    username=current_user.username,
    forename=current_user.forename,
    surname=current_user.surname,
    date=datetime.now(),
    cohort_year=current_user.year,
    form_summ=test.test_type,
    res_module=module.code, 
    Q1_mark = q1_mark,
    Q1_attempts = q1_attempts,
    Q2_mark = q2_mark,
    Q2_attempts = q2_attempts,
    Q3_mark = q3_mark,
    Q3_attempts = q3_attempts,
    Q4_mark = q4_mark,
    Q4_attempts = q4_attempts,
    Q5_mark = q5_mark,
    Q5_attempts = q5_attempts,
    total_mark=marks,
    test_rating=test.rating,
    test_weighting=weight)
    db.session.add(result_sum)
    db.session.commit()
    flash('Test Submit Succesful!')
    return redirect(url_for('index'))
  return render_template('attempt_test.html',title='Attempt Test',form=form,test=test,question_1=question_1,question_2=question_2,question_3=question_3,question_4=question_4,question_5=question_5, module=module)

#######################################################################
    # SP - lecturer Stats - Summative results page
#######################################################################
@app.route("/results_s", methods=['GET'])
@login_required
def results_s():
    # get user information and count of users 
    user = User.query.all()
    unique_user_ids = User.query.distinct(User.id).count()

    # get all summative results
    entries = Results_sum.query.filter_by(form_summ=1).all()

    # Total Mark stats for the user
    all_total_marks = db.session.query(func.round(func.avg(Results_sum.total_mark), 1).label('average_mark'), 
                            func.min(Results_sum.total_mark).label('min_mark'), 
                            func.max(Results_sum.total_mark).label('max_mark'), 
                            func.count(Results_sum.total_mark).label('count_mark')
                            ).filter(Results_sum.form_summ == 1).first()

    total_mark_avg = all_total_marks.average_mark
    total_mark_min = all_total_marks.min_mark
    total_mark_max = all_total_marks.max_mark
    total_mark_count = all_total_marks.count_mark

    # num of students completing summ test
    num_users_with_results = Results_sum.query.filter(Results_sum.form_summ == 1).with_entities(func.count(Results_sum.user_id.distinct())).scalar()

    # calculate the percentage of users with results
    percentage_users_with_results = round((num_users_with_results / unique_user_ids) * 100, 2)

    #######################################################################
    # box plot showing min, max and average Total Marks per cohort year
    #######################################################################
    
    results3 = db.session.query(Results_sum.cohort_year,func.min(Results_sum.total_mark).label('min'), func.max(Results_sum.total_mark).label('max'),
    func.avg(Results_sum.total_mark).label('avg')).filter(Results_sum.form_summ == 1).group_by(Results_sum.cohort_year).all()
    
    fig3 = px.box(results3, x='cohort_year', y=['min', 'max', 'avg'], labels={'value': 'Total Mark', 'cohort_year': 'Cohort Year'},
    title='Total Mark Distribution by Cohort Year')
    fig3.update_layout(xaxis=dict(tickangle=45, linecolor='grey'), yaxis=dict(linecolor='grey',gridcolor='lightgrey'), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='black'))
    fig3.update_yaxes(range=[0, 100])
    fig3.update_layout(yaxis_title='Total Mark (%)')

    #######################################################################
    # scatter plot showing min, max and average Total Marks per cohort year
    #######################################################################

    # adapted from https://stackoverflow.com/questions/63197693/avg-min-max-chart-in-plotly
    # accessed 31-03-2023

    results4 = Results_sum.query.filter(Results_sum.form_summ==1).with_entities(Results_sum.total_mark, Results_sum.cohort_year).all()
    df4 = pd.DataFrame(results4, columns=['total_mark', 'cohort_year'])
    grouped_df = df4.groupby('cohort_year').agg({'total_mark': ['min', 'max', 'mean']})
    fig4 = go.Figure()

    fig4.add_trace(go.Scatter(
        x=grouped_df.index.tolist(),
        y=grouped_df['total_mark']['min'],
        mode="markers", showlegend=False, marker=dict(color="blue", size=10), 
        name='Min'
    ))

    fig4.add_trace(go.Scatter(
        x=grouped_df.index.tolist(),
        y=grouped_df['total_mark']['max'],
        mode="markers", showlegend=False, marker=dict(color="blue", size=10),
        name='Max'
    ))

    fig4.add_trace(go.Scatter(
        x=grouped_df.index.tolist(),
        y=grouped_df['total_mark']['mean'],
        mode="markers", showlegend=False, marker=dict(color="blue", size=15),
        name='Average'
    ))

    # Add a line trace for min and max
    fig4.add_trace(go.Scatter(
        x=grouped_df.index.tolist(),
        y=[(min_val+max_val)/2 for min_val, max_val in zip(grouped_df['total_mark']['min'], grouped_df['total_mark']['max'])],
        mode="lines", showlegend=False, line=dict(color="red", width=2),
        name='Min-Max Line'
    ))

    # # # Add a vertical line between the min and max values for each cohort year
    # for i, row in grouped_df.iterrows():
    #     fig4.add_shape(
    #         type="line",
    #         xref="x",
    #         yref="y",
    #         x0=i,
    #         y0=row['total_mark']['min'],
    #         x1=i,
    #         y1=row['total_mark']['max'],
    #         line=dict(color='cornflowerblue', width=2)
    #     )

    fig4.update_layout(
        title='Total Mark vs Cohort Year',
        xaxis_title='Cohort Year',
        yaxis_title='Total Mark', 
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickangle=45, linecolor='grey'),
        yaxis=dict(linecolor='grey', gridcolor='lightgray')
    )

    fig4.update_yaxes(range=[0, 100])
    fig4.update_layout(yaxis_title='Total Mark (%)')

    plot_div = opy.plot(fig4, auto_open=False, output_type='div')
  
    
    
    return render_template('results_s.html', title='Results', user=user, unique_user_ids=unique_user_ids, entries=entries, num_users_with_results=num_users_with_results, percentage_users_with_results=percentage_users_with_results, total_mark_min=total_mark_min, total_mark_max=total_mark_max, total_mark_avg=total_mark_avg, total_mark_count=total_mark_count, fig3=fig3, plot_div=plot_div)

# SP - lecturer Stats - individual students results page
@app.route("/results_s/<int:user_id>", methods=['GET'])
@login_required
def results_student(user_id):

    # get user information 
    user = User.query.get(user_id)

    # query the DB for the user & their entries
    individ_results = Results_sum.query.filter_by(user_id=user_id).first_or_404()
    entries = Results_sum.query.filter_by(user_id=user_id, form_summ=1).all()
        
    # Total Mark stats for the user
    user_total_marks = db.session.query(func.avg(Results_sum.total_mark).label('average_mark'), 
                            func.min(Results_sum.total_mark).label('min_mark'), 
                            func.max(Results_sum.total_mark).label('max_mark'), 
                            func.count(Results_sum.total_mark).label('count_mark')
                            ).filter(Results_sum.user_id == user_id, Results_sum.form_summ == 1).first()

    total_mark_avg = user_total_marks.average_mark
    total_mark_min = user_total_marks.min_mark
    total_mark_max = user_total_marks.max_mark
    total_mark_count = user_total_marks.count_mark

    # chart_data = analyze_data(entries)
    results = Results_sum.query.filter_by(user_id=user_id, form_summ=1).order_by(Results_sum.date.desc()).limit(10).all()
    dates = [result.date.strftime('%Y-%m-%d') for result in results]
    marks = [result.total_mark for result in results]

    # Query the database to get the data for the plots
    data = Results_sum.query.filter_by(user_id=user_id, form_summ=1).all()
    
    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame([(d.test_id, d.total_mark) for d in data], columns=['test_id', 'total_mark'])
    
    # Determine the selected axis
    selected_axis = request.args.get('axis', 'test_id')
    
    # Create the first Plotly chart
    fig1 = px.scatter(df, x=selected_axis, y='total_mark', title='Test Scores')
    
    # Create the second Plotly chart
    fig2 = px.bar(df, x=selected_axis, y='total_mark', title='Total Marks')
    
    # Create the dropdown options for changing the plot axis
    dropdown_options = [{'label': 'Test ID', 'value': 'test_id'}, {'label': 'Total Mark', 'value': 'total_mark'}]

    
    # Render the dashboard template and pass the data for the plots and dropdown to it
    return render_template('res_student.html', title='Student results', user=user, individ_results=individ_results, entries=entries, 
        user_id=user_id, total_mark_min=total_mark_min, total_mark_max=total_mark_max, total_mark_avg=total_mark_avg, total_mark_count=total_mark_count, results=results, dates=dates, marks=marks, fig1=fig1, fig2=fig2, dropdown_options=dropdown_options)




# SP - lecturer Stats - FORMATIVE results page 
@app.route("/results_form", methods=['GET'])
@login_required
def results_form():
    
    # count of students  
    unique_user_ids = User.query.distinct(User.id).count()

     # get all formative results
    entries = Results_sum.query.filter_by(form_summ=0).group_by(Results_sum.test_id).all()
    

    # create a list to store the calculated results for each test
    test_results = []
    questions_test_results = []
    
    
    for entry in entries:
        # get the count of unique users who attempted the test
        unique_user_count = Results_sum.query.filter_by(form_summ=0, test_id=entry.test_id).with_entities(func.count(distinct(Results_sum.user_id))).scalar()

        # get the count of each question attempted for each unique test_id
        q1_attempts_count = Results_sum.query.filter_by(form_summ=0, test_id=entry.test_id).with_entities(func.count(Results_sum.Q1_attempts)).scalar()
        q2_attempts_count = Results_sum.query.filter_by(form_summ=0, test_id=entry.test_id).with_entities(func.count(Results_sum.Q2_attempts)).scalar()
        q3_attempts_count = Results_sum.query.filter_by(form_summ=0, test_id=entry.test_id).with_entities(func.count(Results_sum.Q3_attempts)).scalar()
        q4_attempts_count = Results_sum.query.filter_by(form_summ=0, test_id=entry.test_id).with_entities(func.count(Results_sum.Q4_attempts)).scalar()
        q5_attempts_count = Results_sum.query.filter_by(form_summ=0, test_id=entry.test_id).with_entities(func.count(Results_sum.Q5_attempts)).scalar()

        # get the number to times each question answered correctly for each unique test_id
        q1_attempts_sum = Results_sum.query.filter_by(form_summ=0, test_id=entry.test_id).with_entities(func.sum(Results_sum.Q1_attempts)).scalar()
        q2_attempts_sum = Results_sum.query.filter_by(form_summ=0, test_id=entry.test_id).with_entities(func.sum(Results_sum.Q2_attempts)).scalar()
        q3_attempts_sum = Results_sum.query.filter_by(form_summ=0, test_id=entry.test_id).with_entities(func.sum(Results_sum.Q3_attempts)).scalar()
        q4_attempts_sum = Results_sum.query.filter_by(form_summ=0, test_id=entry.test_id).with_entities(func.sum(Results_sum.Q4_attempts)).scalar()
        q5_attempts_sum = Results_sum.query.filter_by(form_summ=0, test_id=entry.test_id).with_entities(func.sum(Results_sum.Q5_attempts)).scalar()

        # get the number to times each question answered correctly for each unique test_id
        q1_attempts_wrong = q1_attempts_count - q1_attempts_sum
        q2_attempts_wrong = q2_attempts_count - q2_attempts_sum
        q3_attempts_wrong = q3_attempts_count - q3_attempts_sum
        q4_attempts_wrong = q4_attempts_count - q4_attempts_sum
        q5_attempts_wrong = q5_attempts_count - q5_attempts_sum

        # calculate the percentage of question attempts answered correctly for each unique test_id
        q1_percent = round((q1_attempts_sum / q1_attempts_count) * 100, 2) if q1_attempts_count else 0
        q2_percent = round((q2_attempts_sum / q2_attempts_count) * 100, 2) if q2_attempts_count else 0
        q3_percent = round((q3_attempts_sum / q3_attempts_count) * 100, 2) if q3_attempts_count else 0
        q4_percent = round((q4_attempts_sum / q4_attempts_count) * 100, 2) if q4_attempts_count else 0
        q5_percent = round((q5_attempts_sum / q5_attempts_count) * 100, 2) if q5_attempts_count else 0

        # store the results in the test_results list
        test_results.append({
            'test_id': entry.test_id,
            'unique_user_count': unique_user_count,
            'q1_attempts_count': q1_attempts_count,
            'q2_attempts_count': q2_attempts_count,
            'q3_attempts_count': q3_attempts_count,
            'q4_attempts_count': q4_attempts_count,
            'q5_attempts_count': q5_attempts_count,
            'q1_attempts_sum': q1_attempts_sum,
            'q2_attempts_sum': q2_attempts_sum,
            'q3_attempts_sum': q3_attempts_sum,
            'q4_attempts_sum': q4_attempts_sum,
            'q5_attempts_sum': q5_attempts_sum,
            'q1_attempts_wrong': q1_attempts_wrong,
            'q2_attempts_wrong': q2_attempts_wrong,
            'q3_attempts_wrong': q3_attempts_wrong,
            'q4_attempts_wrong': q4_attempts_wrong,
            'q5_attempts_wrong': q5_attempts_wrong,
            'q1_percent': q1_percent,
            'q2_percent': q2_percent,
            'q3_percent': q3_percent,
            'q4_percent': q4_percent,
            'q5_percent': q5_percent
        })

        # store the results in the test_results list (for each question)
        questions_test_results.append({
            'test_id': entry.test_id,
            'unique_user_count': unique_user_count,
            'q1_attempts_sum': q1_attempts_sum,
            'q1_attempts_wrong': q1_attempts_wrong,
            'q2_attempts_sum': q2_attempts_sum,
            'q2_attempts_wrong': q2_attempts_wrong,
            'q3_attempts_sum': q3_attempts_sum,
            'q3_attempts_wrong': q3_attempts_wrong,
            'q4_attempts_sum': q4_attempts_sum,
            'q4_attempts_wrong': q4_attempts_wrong,
            'q5_attempts_sum': q5_attempts_sum,
            'q5_attempts_wrong': q5_attempts_wrong
        })

    # count the unique test_ids (where form_summ = 0) appearing in DB
    num_test_ids = len(test_results)

    # num of students completing summ test
    num_users_with_results = Results_sum.query.filter(Results_sum.form_summ == 0).with_entities(func.count(Results_sum.user_id.distinct())).scalar()

    # calculate the percentage of users with results
    percentage_users_with_results = round((num_users_with_results / unique_user_ids) * 100, 2)


    # Create a list of unique test ids
    unique_test_ids = [entry.test_id for entry in entries]


    # get selected test id from query string parameter, default to 's16' if not specified
    selected_test_id = request.args.get('test_id', 's15')

    
    ########################################
    # number of times students have completed test 
    ########################################

    plot15_data = db.session.query(Results_sum.user_id, Results_sum.test_id, func.count(Results_sum.id)).filter(Results_sum.form_summ == 0).group_by(Results_sum.user_id, Results_sum.test_id).all()
    # Convert the Rows to a list of tuples
    plot15_results = [tuple(row) for row in plot15_data]

    plot15_dict = {}
    for data in plot15_data:
        if data[1] not in plot15_dict:
            plot15_dict[data[1]] = {}
        total_count = data[2]
        for count in range(1, total_count+1):
            if count not in plot15_dict[data[1]]:
                plot15_dict[data[1]][count] = []
            if count <= total_count:
                plot15_dict[data[1]][count].append(data[0])


    return render_template('results_form.html', title='Results', entries=entries, unique_user_ids=unique_user_ids, unique_test_ids=unique_test_ids, 
        test_results=test_results, questions_test_results=questions_test_results, num_users_with_results=num_users_with_results, 
        percentage_users_with_results=percentage_users_with_results, selected_test_id=selected_test_id,plot15_dict=plot15_dict)
    


    if form.validate_on_submit():
        if form.answer_1.data =="1":
            marks+=question_1.marks
        if form.answer_2.data =="1":
            marks+=question_2.marks
        if form.answer_3.data =="1":
            marks+=question_3.marks
        if form.answer_4.data =="1":
            marks+=question_4.marks
        if form.answer_5.data =="1":
            marks+=question_5.marks
        formative_attempt=FormativeAttempt(test_id=test.test_id,user_id=current_user.id,answer_1=form.answer_1.data,answer_2=form.answer_2.data,answer_3=form.answer_3.data,answer_4=form.answer_4.data,answer_5=form.answer_5.data,question_id_1=question_1.id,question_id_2=question_2.id,question_id_3=question_3.id,question_id_4=question_4.id,question_id_5=question_5.id, marks=marks)
        db.session.add(formative_attempt)
        db.session.commit()
        flash('Test Submit Succesful!')
        return redirect(url_for('index'))
    return render_template('attempt_test.html',title='Attempt Test',form=form,test=test,question_1=question_1,question_2=question_2,question_3=question_3,question_4=question_4,question_5=question_5, marks=marks)


#to allow lect. to choose if its formative or summative - RJ 
@app.route('/choose_create_test', methods=['GET', 'POST'])
@login_required
def choose_create_test():
    form = TestChoice()
    form.question_module.choices = [(module.id, module.name) for module in Module.query.all()]
    if form.test_type.data == 'Formative':
        if form.validate_on_submit():
            formtest= Formativetest(
            author=current_user.id,
            module_code = form.question_module.data,
            testtitle = form.test_title.data,
            test_rating_num = 0
            #Test_feedback = ''
            )
            db.session.add(formtest)
            db.session.commit()
            flash('Your test is added!')
            return redirect('/create_form_test')
    else:
        if form.validate_on_submit():
            return redirect('/create_test')

    return render_template('choose_create_test.html', title = 'Create New Assesment', form=form)

#this allows questions to be added to formative test(sorry about how long it is) - RJ
@app.route('/create_form_test', methods=['GET', 'POST'])
@login_required
def create_form_test():

    test = Formativetest.query.order_by(Formativetest.id.desc()).first()
    test_diff = []
    QCform = QChoiceForm() 

    if QCform.validate_on_submit(): 
        add_question_1()
        questions = test.linkedquestions
        if len(questions) == 1:
            question_1 = questions[-1]
            test_diff.append(question_1.rating_num)
        add_question_2()
        questions = test.linkedquestions 
        if len(questions) == 2:
            question_2 = questions[-1]
            test_diff.append(question_2.rating_num)
        add_question_3()
        questions = test.linkedquestions
        if len(questions) == 3:
            question_3 = questions[-1]
            test_diff.append(question_3.rating_num)
        add_question_4()
        questions = test.linkedquestions
        if len(questions) == 4:
            question_4 = questions[-1]
            test_diff.append(question_4.rating_num)
        add_question_5()
        questions = test.linkedquestions
        if len(questions) == 5:
            question_5 = questions[-1]
            test_diff.append(question_5.rating_num)  
        
        #test.Test_feedback = QCform.Test_feedback.data
        tdlisttotal = sum(test_diff)
        test_rating = tdlisttotal / len(test_diff)
        test.test_rating_num = test_rating
        db.session.commit()
        flash('test added')
        return redirect('/Formative_test_list')


    return render_template('create_form_test.html', title = 'Create Formative Assesment', QCform=QCform, test=test)

#rj
@app.route("/Random_Formative_test", methods=['POST'])
@login_required
def random_formtest():
    test = Formativetest.query.order_by(Formativetest.id.desc()).first()
    totalquestions = Multiplechoice.query.count()
    randomqlist = random.sample(range(2, totalquestions+1), 5)
    test_diff = []

    q1index = randomqlist[0]
    q2index = randomqlist[1]
    q3index = randomqlist[2]
    q4index = randomqlist[3]
    q5index = randomqlist[4]

    question_1 = Multiplechoice.query.filter_by(id = q1index).first()
    test.linkedquestions.append(question_1)
    test_diff.append(question_1.rating_num)
    question_2 = Multiplechoice.query.filter_by(id = q2index).first()
    test.linkedquestions.append(question_2)
    test_diff.append(question_2.rating_num)
    question_3 = Multiplechoice.query.filter_by(id = q3index).first()
    test.linkedquestions.append(question_3)
    test_diff.append(question_3.rating_num)
    question_4 = Multiplechoice.query.filter_by(id = q4index).first()
    test.linkedquestions.append(question_4)
    test_diff.append(question_4.rating_num)
    question_5 = Multiplechoice.query.filter_by(id = q5index).first()
    test.linkedquestions.append(question_5)
    test_diff.append(question_5.rating_num)
    tdlisttotal = sum(test_diff)
    test_rating = tdlisttotal / len(test_diff)
    test.test_rating_num = test_rating
    db.session.commit()

    return redirect('/Formative_test_list')

#rj
@app.route("/Formative_test_list", methods=['GET'])
def formtests():
    allFormtests = Formativetest.query.all()
    return render_template('Formative_test_list.html', title = 'Formative tests list', allFormtests=allFormtests)
#rj
@app.route("/Formative_test/<int:Form_test_id>", methods=['GET'])
def formtest(Form_test_id):
    formtest = Formativetest.query.get_or_404(Form_test_id)
    formtestquestions = formtest.linkedquestions
    return render_template('Formative_test.html', title = formtest.testtitle , formtest=formtest, formtestquestions=formtestquestions)

@app.route("/Start_Formative_test/<int:Form_test_id>", methods=['GET', 'POST'])
def startformtest(Form_test_id):
    test = Formativetest.query.get_or_404(Form_test_id)
    start = TakeFormTestForm()

    if start.validate_on_submit():
        testres = Results_sum(
        user_id = current_user.id,
        username = current_user.username,
        forename = current_user.forename,
        surname = current_user.surname,
        date = datetime.now(),
        cohort_year = '',
        test_id = test.id,
        form_summ = 0,
        res_module = test.mdls.code,
        Q1_mark = 0,
        Q1_attempts = 0,
        Q2_mark = 0,
        Q2_attempts = 0,
        Q3_mark = 0,
        Q3_attempts = 0,
        Q4_mark = 0,
        Q4_attempts = 0,
        Q5_mark = 0,
        Q5_attempts = 0,
        test_rating = test.test_rating_num,
        test_weighting = 1,
        )
        db.session.add(testres)
        db.session.commit()
        flash('Your test has started!')
        return redirect(url_for('takeformtest', Form_test_id=Form_test_id))
    
    return render_template('Start_Formative_test.html', title = 'Start: ' + test.testtitle , test=test, start=start)

#rj
@app.route("/Take_Formative_test/<int:Form_test_id>", methods=['GET', 'POST'])
def takeformtest(Form_test_id):
    test = Formativetest.query.get_or_404(Form_test_id)
    questions = test.linkedquestions
    blank = Multiplechoice.query.filter_by(question='-').first()
    q1answers = Q1TakeFormTestForm()
    q2answers = Q2TakeFormTestForm()
    q3answers = Q3TakeFormTestForm()
    q4answers = Q4TakeFormTestForm()
    q5answers = Q5TakeFormTestForm()
    finish = FinishFormTestForm()
    if len(questions) == 5:
        question_1 = questions[0]
        question_2 = questions[1]
        question_3 = questions[2]
        question_4 = questions[3]
        question_5 = questions[4]
    if len(questions) == 4:
        question_1 = questions[0]
        question_2 = questions[1]
        question_3 = questions[2]
        question_4 = questions[3]
        question_5 = blank
    if len(questions) == 3:
        question_1 = questions[0]
        question_2 = questions[1]
        question_3 = questions[2]
        question_4 = blank
        question_5 = blank
    if len(questions) == 2:
        question_1 = questions[0]
        question_2 = questions[1]
        question_3 = blank
        question_4 = blank
        question_5 = blank
    if len(questions) == 1:
        question_1 = questions[0]
        question_2 = blank
        question_3 = blank
        question_4 = blank
        question_5 = blank
    if len(questions) == 0:
        question_1 = blank
        question_2 = blank
        question_3 = blank
        question_4 = blank
        question_5 = blank
    
        
    lastres = Results_sum.query.order_by(Results_sum.id.desc()).first()

    if q1answers.q1_submit.data and q1answers.validate():
        if question_1.question_type == 'Multiplechoice':
            if question_1.ans_choice_1 == True and q1answers.q1_ans_multi_select_1.data == True:
                lastres.Q1_mark = 100
                lastres.Q1_attempts = lastres.Q1_attempts + 1
            if question_1.ans_choice_1 == False and q1answers.q1_ans_multi_select_1.data == True:
                lastres.Q1_mark = 0
                flash('Incorrect - Try again')
                lastres.Q1_attempts = lastres.Q1_attempts + 1
            if question_1.ans_choice_2 == True and q1answers.q1_ans_multi_select_2.data == True:
                lastres.Q1_mark = 100
                lastres.Q1_attempts = lastres.Q1_attempts + 1
            if question_1.ans_choice_2 == False and q1answers.q1_ans_multi_select_2.data == True:
                lastres.Q1_mark = 0
                flash('Incorrect - Try again')
                lastres.Q1_attempts = lastres.Q1_attempts + 1
            if question_1.ans_choice_3 == True and q1answers.q1_ans_multi_select_3.data == True:
                lastres.Q1_mark = 100
                lastres.Q1_attempts = lastres.Q1_attempts + 1
            if question_1.ans_choice_3 == False and q1answers.q1_ans_multi_select_3.data == True:
                lastres.Q1_mark = 0
                flash('Incorrect - Try again')
                lastres.Q1_attempts = lastres.Q1_attempts + 1
            if question_1.ans_choice_4 == True and q1answers.q1_ans_multi_select_4.data == True:
                lastres.Q1_mark = 100
                lastres.Q1_attempts = lastres.Q1_attempts + 1
            if question_1.ans_choice_1 == False and q1answers.q1_ans_multi_select_1.data == True:
                lastres.Q1_mark = 0
                lastres.Q1_attempts = lastres.Q1_attempts + 1
                flash('Incorrect - Try again')
        else:
            if question_1.answer_1 == q1answers.q1_ans_FTG.data:
                lastres.Q1_mark = 0
                lastres.Q1_attempts = lastres.Q1_attempts + 1
            if question_1.answer_1 != q1answers.q1_ans_FTG.data:
                lastres.Q1_mark = 0
                lastres.Q1_attempts = lastres.Q1_attempts + 1
                flash('Incorrect - Try again')
        db.session.commit()

    if q2answers.q2_submit.data and q2answers.validate():
        if question_2.question_type == 'Multiplechoice':
            if question_2.ans_choice_1 == True and q2answers.q2_ans_multi_select_1.data == True:
                lastres.Q2_mark = 100
                lastres.Q2_attempts = lastres.Q2_attempts + 1
            if question_2.ans_choice_1 == False and q2answers.q2_ans_multi_select_1.data == True:
                lastres.Q2_mark = 0
                flash('Incorrect - Try again')
                lastres.Q2_attempts = lastres.Q2_attempts + 1
            if question_2.ans_choice_2 == True and q2answers.q2_ans_multi_select_2.data == True:
                lastres.Q2_mark = 100
                lastres.Q2_attempts = lastres.Q2_attempts + 1
            if question_2.ans_choice_2 == False and q2answers.q2_ans_multi_select_2.data == True:
                lastres.Q2_mark = 0
                flash('Incorrect - Try again')
                lastres.Q2_attempts = lastres.Q2_attempts + 1
            if question_2.ans_choice_3 == True and q2answers.q2_ans_multi_select_3.data == True:
                lastres.Q2_mark = 100
                lastres.Q2_attempts = lastres.Q2_attempts + 1
            if question_2.ans_choice_3 == False and q2answers.q2_ans_multi_select_3.data == True:
                lastres.Q2_mark = 0
                lastres.Q2_attempts = lastres.Q2_attempts + 1
                flash('Incorrect - Try again')
            if question_2.ans_choice_4 == True and q2answers.q2_ans_multi_select_4.data == True:
                lastres.Q2_mark = 100
                lastres.Q2_attempts = lastres.Q2_attempts + 1
            if question_2.ans_choice_1 == False and q2answers.q2_ans_multi_select_1.data == True:
                lastres.Q2_mark = 0
                lastres.Q2_attempts = lastres.Q2_attempts + 1
                flash('Incorrect - Try again')
        else:
            if question_2.answer_1 == q2answers.q2_ans_FTG.data:
                lastres.Q2_mark = 0
                lastres.Q2_attempts = lastres.Q2_attempts + 1
            if question_2.answer_1 != q2answers.q2_ans_FTG.data:
                lastres.Q2_mark = 0
                lastres.Q2_attempts = lastres.Q2_attempts + 1
                flash('Incorrect - Try again')
        db.session.commit()
    
    if q3answers.q3_submit.data and q3answers.validate():
        if question_3.question_type == 'Multiplechoice':
            if question_3.ans_choice_1 == True and q3answers.q3_ans_multi_select_1.data == True:
                lastres.Q3_mark = 100
                lastres.Q3_attempts = lastres.Q3_attempts + 1
            if question_3.ans_choice_1 == False and q3answers.q3_ans_multi_select_1.data == True:
                lastres.Q3_mark = 0
                flash('Incorrect - Try again')
                lastres.Q3_attempts = lastres.Q3_attempts + 1
            if question_3.ans_choice_2 == True and q3answers.q3_ans_multi_select_2.data == True:
                lastres.Q3_mark = 100
                lastres.Q3_attempts = lastres.Q3_attempts + 1
            if question_3.ans_choice_2 == False and q3answers.q3_ans_multi_select_2.data == True:
                lastres.Q3_mark = 0
                flash('Incorrect - Try again')
                lastres.Q3_attempts = lastres.Q3_attempts + 1
            if question_3.ans_choice_3 == True and q3answers.q3_ans_multi_select_3.data == True:
                lastres.Q3_mark = 100
                lastres.Q3_attempts = lastres.Q3_attempts + 1
            if question_3.ans_choice_3 == False and q3answers.q3_ans_multi_select_3.data == True:
                lastres.Q3_mark = 0
                flash('Incorrect - Try again')
                lastres.Q3_attempts = lastres.Q3_attempts + 1
            if question_3.ans_choice_4 == True and q3answers.q3_ans_multi_select_4.data == True:
                lastres.Q3_mark = 100
                lastres.Q3_attempts = lastres.Q3_attempts + 1
            if question_3.ans_choice_1 == False and q3answers.q3_ans_multi_select_1.data == True:
                lastres.Q3_mark = 0
                lastres.Q3_attempts = lastres.Q3_attempts + 1
                flash('Incorrect - Try again')
        else:
            if question_3.answer_1 == q3answers.q3_ans_FTG.data:
                lastres.Q3_mark = 0
                lastres.Q3_attempts = lastres.Q3_attempts + 1
            if question_3.answer_1 != q3answers.q3_ans_FTG.data:
                lastres.Q3_mark = 0
                lastres.Q3_attempts = lastres.Q3_attempts + 1
                flash('Incorrect - Try again')
        db.session.commit()
    
    if q4answers.q4_submit.data and q4answers.validate():
        if question_4.question_type == 'Multiplechoice':
            if question_4.ans_choice_1 == True and q4answers.q4_ans_multi_select_1.data == True:
                lastres.Q4_mark = 100
                lastres.Q4_attempts = lastres.Q4_attempts + 1
            if question_4.ans_choice_1 == False and q4answers.q4_ans_multi_select_1.data == True:
                lastres.Q4_mark = 0
                flash('Incorrect - Try again')
                lastres.Q4_attempts = lastres.Q4_attempts + 1
            if question_4.ans_choice_2 == True and q4answers.q4_ans_multi_select_2.data == True:
                lastres.Q4_mark = 100
                lastres.Q4_attempts = lastres.Q4_attempts + 1
            if question_4.ans_choice_2 == False and q4answers.q4_ans_multi_select_2.data == True:
                lastres.Q4_mark = 0
                flash('Incorrect - Try again')
                lastres.Q4_attempts = lastres.Q4_attempts + 1
            if question_4.ans_choice_3 == True and q4answers.q4_ans_multi_select_3.data == True:
                lastres.Q4_mark = 100
                lastres.Q4_attempts = lastres.Q4_attempts + 1
            if question_4.ans_choice_3 == False and q4answers.q4_ans_multi_select_3.data == True:
                lastres.Q4_mark = 0
                flash('Incorrect - Try again')
                lastres.Q4_attempts = lastres.Q4_attempts + 1
            if question_4.ans_choice_4 == True and q4answers.q4_ans_multi_select_4.data == True:
                lastres.Q4_mark = 100
                lastres.Q4_attempts = lastres.Q4_attempts + 1
            if question_4.ans_choice_1 == False and q4answers.q4_ans_multi_select_1.data == True:
                lastres.Q4_mark = 0
                lastres.Q4_attempts = lastres.Q4_attempts + 1
                flash('Incorrect - Try again')
        else:
            if question_4.answer_1 == q4answers.q4_ans_FTG.data:
                lastres.Q4_mark = 0
                lastres.Q4_attempts = lastres.Q4_attempts + 1
            if question_4.answer_1 != q4answers.q4_ans_FTG.data:
                lastres.Q4_mark = 0
                lastres.Q4_attempts = lastres.Q4_attempts + 1
                flash('Incorrect - Try again')
        db.session.commit()

    if q5answers.q5_submit.data and q5answers.validate():
        if question_5.question_type == 'Multiplechoice':
            if question_5.ans_choice_1 == True and q5answers.q5_ans_multi_select_1.data == True:
                lastres.Q5_mark = 100
                lastres.Q5_attempts = lastres.Q5_attempts + 1
            if question_5.ans_choice_1 == False and q5answers.q5_ans_multi_select_1.data == True:
                lastres.Q5_mark = 0
                flash('Incorrect - Try again')
                lastres.Q5_attempts = lastres.Q5_attempts + 1
            if question_5.ans_choice_2 == True and q5answers.q5_ans_multi_select_2.data == True:
                lastres.Q5_mark = 100
                lastres.Q5_attempts = lastres.Q5_attempts + 1
            if question_5.ans_choice_2 == False and q5answers.q5_ans_multi_select_2.data == True:
                lastres.Q5_mark = 0
                flash('Incorrect - Try again')
                lastres.Q5_attempts = lastres.Q5_attempts + 1
            if question_5.ans_choice_3 == True and q5answers.q5_ans_multi_select_3.data == True:
                lastres.Q5_mark = 100
                lastres.Q5_attempts = lastres.Q5_attempts + 1
            if question_5.ans_choice_3 == False and q5answers.q5_ans_multi_select_3.data == True:
                lastres.Q5_mark = 0
                lastres.Q5_attempts = lastres.Q5_attempts + 1
                flash('Incorrect - Try again')
            if question_5.ans_choice_4 == True and q5answers.q5_ans_multi_select_4.data == True:
                lastres.Q5_mark = 100
                lasres.Q5_attempts = lastres.Q5_attempts + 1
            if question_5.ans_choice_1 == False and q5answers.q5_ans_multi_select_1.data == True:
                lastres.Q5_mark = 0
                lastres.Q5_attempts = lastres.Q5_attempts + 1
                flash('Incorrect - Try again')
        else:
            if question_5.answer_1 == q5answers.q5_ans_FTG.data:
                lastres.Q5_mark = 100
                lastres.Q5_attempts = lastres.Q5_attempts + 1
            if question_5.answer_1 != q5answers.q5_ans_FTG.data:
                lastres.Q5_mark = 0
                lastres.Q5_attempts = lastres.Q5_attempts + 1
                flash('Incorrect - Try again')
        db.session.commit()

    if finish.submitF.data and finish.validate():
        list = []
        if question_1.question != '-':
            list.append(lastres.Q1_mark)
        if question_2.question != '-':
            list.append(lastres.Q2_mark)
        if question_3.question != '-':
            list.append(lastres.Q3_mark)
        if question_4.question != '-':
            list.append(lastres.Q4_mark)
        if question_5.question != '-':
            list.append(lastres.Q5_mark)
        listtotal = sum(list)
        length = len(list)
        total_mark_sum = listtotal / length
        lastres.total_mark = total_mark_sum
        db.session.commit()
        return redirect('/results_s')

    return render_template('Take_Formative_test.html', title = 'Take: ' + test.testtitle , test=test, questions=questions, q1answers=q1answers, q2answers=q2answers, q3answers=q3answers, q4answers=q4answers, q5answers=q5answers, finish=finish, question_1=question_1, question_2=question_2, question_3=question_3, question_4=question_4, question_5=question_5, lastres=lastres)
#rj
@app.route("/Formative_test/<int:Form_test_id>/delete", methods=['POST'])
@login_required
def delete_formtest(Form_test_id):
  test = Formativetest.query.get_or_404(Form_test_id)
  db.session.delete(test)
  db.session.commit()
  flash('Your Post has been deleted')
  return redirect('/Formative_test_list')

@app.route("/Formative_test/<int:Form_test_id>/release", methods=['POST'])
@login_required
def release_formtest(Form_test_id):
    test = Formativetest.query.get_or_404(Form_test_id)
    if test.available_to_take == True:
        test.available_to_take = False
    else:
        test.available_to_take = True
    db.session.commit()
    return redirect('/Formative_test_list')

#EMMA
''' @app.route("/your_results", methods=['GET'])
@login_required
def your_results():

    user_id = session.get('user_id')
    individ_results=Results_sum.query.filter_by(user_id=user_id).all()
    return render_template('your_results.html', title = 'Your Results', individ_results = individ_results)'''
