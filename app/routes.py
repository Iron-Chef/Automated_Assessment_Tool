from flask import render_template, flash, redirect, url_for, request, g,session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy import *
from app.models import User,Test, Multiplechoice, Results_sum
from app.forms import LoginForm, CreateTestForm, QuestionForm
from app import app,db

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
    return render_template('index.html', title = 'Home')

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
@app.route('/mc_questions', methods=['GET', 'POST'])
@login_required
def question():
    form=QuestionForm()
    
    if form.validate_on_submit():
        multi= Multiplechoice(
        user_id=current_user.id,
        question=form.question.data, 
        answer_1=form.answer1.data,ans_choice_1=form.ans_multi_select_1.data, 
        answer_2=form.answer2.data,ans_choice_2=form.ans_multi_select_2.data, 
        answer_3=form.answer3.data, ans_choice_3=form.ans_multi_select_3.data,
        answer_4=form.answer4.data, ans_choice_4=form.ans_multi_select_4.data,
        marks=form.marks.data, 
        feedback=form.feedback.data
        )
        db.session.add(multi)
        db.session.commit()
        flash('Your question is added!')
        return redirect('/mc_questions')
    return render_template("mc_questions.html", title="Add Multiple Choice Questions", form=form)

@app.route("/question_list",methods=['GET'])
def result():
    
    questions=Multiplechoice.query.all()
    
        
    return render_template('question_list.html',questions=questions)

@app.route("/results_s", methods=['GET'])
@login_required
def results_s():
    results_sum = Results_sum.query.all()
    num_marked = len(Results_sum.query.all())
    total_mark = Results_sum.query.with_entities(func.sum(Results_sum.mark).label('total')).first().total
    average_mark = int(total_mark/num_marked)

    return render_template('results_s.html', title='Results', results_sum=results_sum, num_marked=num_marked, total_mark=total_mark, average_mark=average_mark)

@app.route("/results_s/<int:user_id>", methods=['GET'])
@login_required
def results_student(user_id):
    
    individ_results = Results_sum.query.filter_by(user_id=user_id).first_or_404()
    entries = Results_sum.query.filter_by(user_id=user_id).all()
    count_entries = len(Results_sum.query.filter_by(user_id=user_id).all())
    return render_template('res_student.html', title='Student results', individ_results=individ_results, entries=entries, count_entries=count_entries)

