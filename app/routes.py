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
from app.models import User,Test, Multiplechoice, FormativeAttempt,Results_sum, Module, Studentanswer
from app.forms import DIFFICULTY_RATING,LoginForm, CreateTestForm, QuestionForm, SubmitAttemptForm, StudentAnswerForm, ResultsForm, FillInTheBlankQuestionForm
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
  form.question_id_1.choices = [(question.id,question.id) for question in questions]
  form.question_id_2.choices = [(question.id,question.id) for question in questions]
  form.question_id_3.choices = [(question.id,question.id) for question in questions]
  form.question_id_4.choices = [(question.id,question.id) for question in questions]
  form.question_id_5.choices = [(question.id,question.id) for question in questions]
  if form.validate_on_submit():
    test=Test(test_type=form.test_type.data,creator_id=current_user.id,question_id_1=form.question_id_1.data,question_id_2=form.question_id_2.data,question_id_3=form.question_id_3.data,question_id_4=form.question_id_4.data,question_id_5=form.question_id_5.data)
    db.session.add(test)
    db.session.commit()
    flash('Test Creation Succesful!')
    return redirect(url_for('index'))
  return render_template('create_test.html',title='Create Test',form=form,questions=questions)

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
        topic_tag = form.topic.data,
        marks=form.marks.data, 
        rating = dict(DIFFICULTY_RATING).get(form.rating.data),
        rating_num= form.rating.data,
        feedback=form.feedback.data,
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
        db.session.delete (mcquestion_to_delete)
        db.session.commit()
        flash("Question deleted!")

        questions=Multiplechoice.query.all()
        return render_template('question_list.html',questions=questions)

    except:
        flash("Problem deleting question, please check with Admin!")

        questions=Multiplechoice.query.all()
        return render_template('question_list.html',questions=questions)

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
    mcquestion=Multiplechoice.query.get_or_404(mc_question_id)
    form=QuestionForm()
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

# Add fill-in-the-blank questions
@app.route("/add_fill_in_the_blank_question", methods = ['GET', 'POST'])
def add_fill_in_the_blank_question():

    form = FillInTheBlankQuestionForm()

    if form.validate_on_submit():

        question = Multiplechoice(
        user_id = current_user.id,
        question = form.question.data, 
        answer_1 = form.answer.data,
        topic_tag = form.topic.data,
        marks = form.marks.data, 
        feedback = form.feedback.data,
        question_type = "fill_in_the_blank"
        )
        db.session.add(question)
        db.session.commit()

    return render_template('add_fill_in_the_blank_question.html', form = form)

#view list of questions- opportunity to list by different queries# Add code-challenge questions
@app.route("/add_code_challenge_question.html", methods = ['GET', 'POST'])
def add_code_challenge_question():
    return render_template('add_code_challenge_question.html')

@app.route("/question_list", methods = ['GET'])
@login_required
def question_list():
    
    questions = Multiplechoice.query.all()
    
    return render_template('question_list.html',questions=questions)

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
  marks=0



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
    func.avg(Results_sum.total_mark).label('avg')).group_by(Results_sum.cohort_year).all()
    
    fig3 = px.box(results3, x='cohort_year', y=['min', 'max', 'avg'], labels={'value': 'Total Mark', 'cohort_year': 'Cohort Year'},
    title='Total Mark Distribution by Cohort Year')
    fig3.update_layout(xaxis=dict(tickangle=45, linecolor='grey'), yaxis=dict(linecolor='grey',gridcolor='lightgrey'), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='black'))
    fig3.update_yaxes(range=[0, 100])

    #######################################################################
    # scatter plot showing min, max and average Total Marks per cohort year
    #######################################################################

    # adapted from https://stackoverflow.com/questions/63197693/avg-min-max-chart-in-plotly
    # accessed 31-03-2023

    results4 = Results_sum.query.with_entities(Results_sum.total_mark, Results_sum.cohort_year).all()
    df4 = pd.DataFrame(results4, columns=['total_mark', 'cohort_year'])
    grouped_df = df4.groupby('cohort_year').agg({'total_mark': ['min', 'max', 'mean']})
    fig4 = go.Figure()

    fig4.add_trace(go.Scatter(
        x=grouped_df.index,
        y=grouped_df['total_mark']['min'],
        mode="markers", showlegend=False, marker=dict(color="blue", size=10), 
        name='Min'
    ))

    fig4.add_trace(go.Scatter(
        x=grouped_df.index,
        y=grouped_df['total_mark']['max'],
        mode="markers", showlegend=False, marker=dict(color="blue", size=10),
        name='Max'
    ))

    fig4.add_trace(go.Scatter(
        x=grouped_df.index,
        y=grouped_df['total_mark']['mean'],
        mode="markers", showlegend=False, marker=dict(color="blue", size=15),
        name='Average'
    ))

    # Add a line trace for min and max
    fig4.add_trace(go.Scatter(
        x=grouped_df.index,
        y=[(min_val+max_val)/2 for min_val, max_val in zip(grouped_df['total_mark']['min'], grouped_df['total_mark']['max'])],
        mode="lines", showlegend=False, line=dict(color="red", width=2),
        name='Min-Max Line'
    ))

    # Add a vertical line between the min and max values for each cohort year
    for i, row in grouped_df.iterrows():
        fig4.add_shape(
            type="line",
            xref="x",
            yref="y",
            x0=i,
            y0=row['total_mark']['min'],
            x1=i,
            y1=row['total_mark']['max'],
            line=dict(color='cornflowerblue', width=2)
        )

    fig4.update_layout(
        title='Total Mark vs Cohort Year',
        xaxis_title='Cohort Year',
        yaxis_title='Total Mark', 
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickangle=45, linecolor='grey'),
        yaxis=dict(linecolor='grey', gridcolor='lightgray')
    )

    fig4.update_yaxes(range=[0, 100])

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
        if data[2] not in plot15_dict[data[1]]:
            plot15_dict[data[1]][data[2]] = []
        plot15_dict[data[1]][data[2]].append(data[0])


    return render_template('results_form.html', title='Results', entries=entries, unique_user_ids=unique_user_ids, unique_test_ids=unique_test_ids, 
        test_results=test_results, questions_test_results=questions_test_results, num_users_with_results=num_users_with_results, 
        percentage_users_with_results=percentage_users_with_results, selected_test_id=selected_test_id,plot15_dict=plot15_dict)
    

