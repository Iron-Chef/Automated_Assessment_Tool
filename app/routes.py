from flask import render_template, flash, redirect, url_for, request, g,session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User, Multiplechoice, FormativeTest
from app.forms import LoginForm, QuestionForm, MCChoiceForm
from app import app, db

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

@app.route('/create_form_test', methods=['GET', 'POST'])
@login_required
def create_form_test():
    form = MCChoiceForm()
    if form.validate_on_submit():
        formtest= FormativeTest(
        author=current_user.id,
        mcquestion_1_id=form.question_1.data.id,
        mcquestion_1=form.question_1.data.question,
        mcquestion_2_id=form.question_2.data.id,
        mcquestion_2=form.question_2.data.question,
        mcquestion_3_id=form.question_3.data.id,
        mcquestion_3=form.question_3.data.question,
        mcquestion_4_id=form.question_4.data.id,
        mcquestion_4=form.question_4.data.question,
        mcquestion_5_id=form.question_5.data.id,
        mcquestion_5=form.question_5.data.question,
        )
        db.session.add(formtest)
        db.session.commit()
        flash('Your test is added!')
        return redirect('/create_form_test')
    return render_template('create_form_test.html', title = 'Create Formative Assesment', form=form)

@app.route("/Formative_test_list",methods=['GET'])
def formtests():
    
    formtests=FormativeTest.query.all()
    
        
    return render_template('Formative_test_list.html',formtests=formtests)
