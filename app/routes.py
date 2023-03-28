from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy import *
from app.models import User,Test, Multiplechoice, FormativeAttempt,Results_sum, Module, Studentanswer
from app.forms import DIFFICULTY_RATING,LoginForm, CreateTestForm, QuestionForm, SubmitAttemptForm, StudentAnswerForm, ResultsForm, FillInTheBlankQuestionForm
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

''' Emma - attempting to separate the types of user at log in stage

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        user_type = retrieve_user_type(username, password)

        if user_type == 'lecturer':
            session['user_type'] = 'lecturer'
            return redirect(url_for('home_lecturer'))
        elif user_type == 'student':
            session['user_type'] = 'student'
            return redirect(url_for('home_student'))
        else:
            flash('Invalid username or password')
        return redirect(url_for('login'))
'''

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


# SP - lecturer Stats - Summative results page 
@app.route("/results_s", methods=['GET'])
@login_required
def results_s():
    results_sum = Results_sum.query.all()
    num_marked = len(Results_sum.query.all())
    total_marks = Results_sum.query.with_entities(func.sum(Results_sum.total_mark).label('total')).first().total
    average_mark = int(total_marks/num_marked)

    return render_template('results_s.html', title='Results', results_sum=results_sum, num_marked=num_marked, total_marks=total_marks, average_mark=average_mark)

# SP - lecturer Stats - individual students results page
@app.route("/results_s/<int:user_id>", methods=['GET'])
@login_required
def results_student(user_id):
    
    individ_results = Results_sum.query.filter_by(user_id=user_id).first_or_404()
    entries = Results_sum.query.filter_by(user_id=user_id).all()
    count_entries = len(Results_sum.query.filter_by(user_id=user_id).all())
    return render_template('res_student.html', title='Student results', individ_results=individ_results, entries=entries, count_entries=count_entries)

''' Emma - Attempting to separate student and lecturer by diverting to 
different 'home' pages once logged in

@app.route('/home_lecturer/lecturer')
def home_lecturer():
    
    return render_template('home_lecturer.html')

@app.route('/home_student/student')
def home_student():
    
    return render_template('home_student.html')
'''

''' Emma - export html table of results to a pdf format using pdf library pdfkit
Have to install >> "pip install fpdf"
Taken from - https://roytuts.com/generate-pdf-report-from-mysql-database-using-python-flask/

@app.route('/export_to_pdf')
def export_to_pdf():
    # get the table of results from your database or form submission
    results = get_results()

    rendered_template = render_template('your_results.html', results=results)

    # create the pdf page view
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }

    # convert the HTML template to PDF using pdfkit
    pdf = pdfkit.from_string(rendered_template, False, options=options)

    # send the PDF file as a response to the user
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=results.pdf'
    return response
'''
