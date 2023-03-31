from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy import *
from datetime import datetime
from app.models import User,Test, Multiplechoice, FormativeAttempt,Results_sum, Module, Studentanswer, Formativetest
from app.forms import DIFFICULTY_RATING,LoginForm, CreateTestForm, QuestionForm, SubmitAttemptForm, StudentAnswerForm, ResultsForm, FillInTheBlankQuestionForm, QChoiceForm, TestChoice, TakeFormTestForm, Q1TakeFormTestForm, Q2TakeFormTestForm, Q3TakeFormTestForm, Q4TakeFormTestForm, Q5TakeFormTestForm, FinishFormTestForm
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

# Add fill-in-the-blank questions
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

    return render_template('add_fill_in_the_blank_question.html', form = form)

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

    return render_template('edit_fill_in_the_blank_question.html', fill_in_the_blank_question = fill_in_the_blank_question, form = form)

@app.route("/fill_in_the_blank_question/delete/<int:fill_in_the_blank_question_id>")
def delete_fill_in_the_blank_question(fill_in_the_blank_question_id):
    fill_in_the_blank_question_to_delete = Multiplechoice.query.get_or_404(fill_in_the_blank_question_id)

    try:
        db.session.delete(fill_in_the_blank_question_to_delete)
        db.session.commit()
        flash("Question deleted!")

        return redirect('/question_list')

    except:
        flash("Problem deleting question, please check with Admin!")

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
            testtitle = form.test_title.data
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
    QCform = QChoiceForm()
    test = Formativetest.query.order_by(Formativetest.id.desc()).first()
    if QCform.validate_on_submit():
        if QCform.question_1.data.question != '-':
            question_1 = QCform.question_1.data
            test.linkedquestions.append(question_1)
        if QCform.WriteMCquestion_1.question.data !='':
            Q1multi= Multiplechoice(
            user_id=current_user.id,
            question=QCform.WriteMCquestion_1.question.data, 
            answer_1=QCform.WriteMCquestion_1.answer1.data,ans_choice_1=QCform.WriteMCquestion_1.ans_multi_select_1.data, 
            answer_2=QCform.WriteMCquestion_1.answer2.data,ans_choice_2=QCform.WriteMCquestion_1.ans_multi_select_2.data, 
            answer_3=QCform.WriteMCquestion_1.answer3.data, ans_choice_3=QCform.WriteMCquestion_1.ans_multi_select_3.data,
            answer_4=QCform.WriteMCquestion_1.answer4.data, ans_choice_4=QCform.WriteMCquestion_1.ans_multi_select_4.data,
            marks=QCform.WriteMCquestion_1.marks.data,
            topic_tag = '',
            feedback=QCform.WriteMCquestion_1.feedback.data,
            question_type = 'Multiplechoice'
            )
            db.session.add(Q1multi)
            db.session.commit()
            question_1 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_1)
        if QCform.WriteFTGquestion_1.question.data !='':
            Q1FTG = Multiplechoice(
            user_id = current_user.id,
            question = QCform.WriteFTGquestion_1.question.data, 
            answer_1 = QCform.WriteFTGquestion_1.answer.data,
            answer_2 = '',
            answer_3 = '',
            answer_4 = '',
            topic_tag = '',
            marks = QCform.WriteFTGquestion_1.marks.data, 
            feedback = QCform.WriteFTGquestion_1.feedback.data,
            question_type = "fill_in_the_blank"
            )
            db.session.add(Q1FTG)
            db.session.commit()
            question_1 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_1)
        if QCform.question_2.data.question != '-':
            question_2 = QCform.question_2.data
            test.linkedquestions.append(question_2)
        if QCform.WriteMCquestion_2.question.data !='':
            Q2multi= Multiplechoice(
            user_id=current_user.id,
            question=QCform.WriteMCquestion_2.question.data, 
            answer_1=QCform.WriteMCquestion_2.answer1.data,ans_choice_1=QCform.WriteMCquestion_2.ans_multi_select_1.data, 
            answer_2=QCform.WriteMCquestion_2.answer2.data,ans_choice_2=QCform.WriteMCquestion_2.ans_multi_select_2.data, 
            answer_3=QCform.WriteMCquestion_2.answer3.data, ans_choice_3=QCform.WriteMCquestion_2.ans_multi_select_3.data,
            answer_4=QCform.WriteMCquestion_2.answer4.data, ans_choice_4=QCform.WriteMCquestion_2.ans_multi_select_4.data,
            marks=QCform.WriteMCquestion_2.marks.data,
            topic_tag = '',
            feedback=QCform.WriteMCquestion_2.feedback.data,
            question_type = 'Multiplechoice'
            )
            db.session.add(Q2multi)
            db.session.commit()
            question_2 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_2)
        if QCform.WriteFTGquestion_2.question.data !='':
            Q2FTG = Multiplechoice(
            user_id = current_user.id,
            question = QCform.WriteFTGquestion_2.question.data, 
            answer_1 = QCform.WriteFTGquestion_2.answer.data,
            answer_2 = '',
            answer_3 = '',
            answer_4 = '',
            topic_tag = '',
            marks = QCform.WriteFTGquestion_2.marks.data, 
            feedback = QCform.WriteFTGquestion_2.feedback.data,
            question_type = "fill_in_the_blank"
            )
            db.session.add(Q2FTG)
            db.session.commit()
            question_2 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_2) 
        if QCform.question_3.data.question != '-':
            question_3 = QCform.question_3.data
            test.linkedquestions.append(question_3) 
        if QCform.WriteMCquestion_3.question.data !='':
            Q3multi= Multiplechoice(
            user_id=current_user.id,
            question=QCform.WriteMCquestion_3.question.data, 
            answer_1=QCform.WriteMCquestion_3.answer1.data,ans_choice_1=QCform.WriteMCquestion_3.ans_multi_select_1.data, 
            answer_2=QCform.WriteMCquestion_3.answer2.data,ans_choice_2=QCform.WriteMCquestion_3.ans_multi_select_2.data, 
            answer_3=QCform.WriteMCquestion_3.answer3.data, ans_choice_3=QCform.WriteMCquestion_3.ans_multi_select_3.data,
            answer_4=QCform.WriteMCquestion_3.answer4.data, ans_choice_4=QCform.WriteMCquestion_3.ans_multi_select_4.data,
            marks=QCform.WriteMCquestion_3.marks.data,
            topic_tag = '',
            feedback=QCform.WriteMCquestion_3.feedback.data,
            question_type = 'Multiplechoice'
            )
            db.session.add(Q3multi)
            db.session.commit()
            question_3 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_3)
        if QCform.WriteFTGquestion_3.question.data !='':
            Q3FTG = Multiplechoice(
            user_id = current_user.id,
            question = QCform.WriteFTGquestion_3.question.data, 
            answer_1 = QCform.WriteFTGquestion_3.answer.data,
            answer_2 = '',
            answer_3 = '',
            answer_4 = '',
            topic_tag = '',
            marks = QCform.WriteFTGquestion_3.marks.data, 
            feedback = QCform.WriteFTGquestion_3.feedback.data,
            question_type = "fill_in_the_blank"
            )
            db.session.add(Q3FTG)
            db.session.commit()
            question_3 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_3) 
        if QCform.question_4.data.question != '-':
            question_4 = QCform.question_4.data
            test.linkedquestions.append(question_4)
        if QCform.WriteMCquestion_4.question.data !='':
            Q4multi= Multiplechoice(
            user_id=current_user.id,
            question=QCform.WriteMCquestion_4.question.data, 
            answer_1=QCform.WriteMCquestion_4.answer1.data,ans_choice_1=QCform.WriteMCquestion_4.ans_multi_select_1.data, 
            answer_2=QCform.WriteMCquestion_4.answer2.data,ans_choice_2=QCform.WriteMCquestion_4.ans_multi_select_2.data, 
            answer_3=QCform.WriteMCquestion_4.answer3.data, ans_choice_3=QCform.WriteMCquestion_4.ans_multi_select_3.data,
            answer_4=QCform.WriteMCquestion_4.answer4.data, ans_choice_4=QCform.WriteMCquestion_4.ans_multi_select_4.data,
            marks=QCform.WriteMCquestion_4.marks.data,
            topic_tag = '',
            feedback=QCform.WriteMCquestion_4.feedback.data,
            question_type = 'Multiplechoice'
            )
            db.session.add(Q4multi)
            db.session.commit()
            question_4 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_4)
        if QCform.WriteFTGquestion_4.question.data !='':
            Q4FTG = Multiplechoice(
            user_id = current_user.id,
            question = QCform.WriteFTGquestion_4.question.data, 
            answer_1 = QCform.WriteFTGquestion_4.answer.data,
            answer_2 = '',
            answer_3 = '',
            answer_4 = '',
            topic_tag = '',
            marks = QCform.WriteFTGquestion_4.marks.data, 
            feedback = QCform.WriteFTGquestion_4.feedback.data,
            question_type = "fill_in_the_blank"
            )
            db.session.add(Q4FTG)
            db.session.commit()
            question_4 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_4) 
        if QCform.question_5.data.question != '-':
            question_5 = QCform.question_5.data
            test.linkedquestions.append(question_5)
        if QCform.WriteMCquestion_5.question.data !='':
            Q5multi= Multiplechoice(
            user_id=current_user.id,
            question=QCform.WriteMCquestion_5.question.data, 
            answer_1=QCform.WriteMCquestion_5.answer1.data,ans_choice_1=QCform.WriteMCquestion_5.ans_multi_select_1.data, 
            answer_2=QCform.WriteMCquestion_5.answer2.data,ans_choice_2=QCform.WriteMCquestion_5.ans_multi_select_2.data, 
            answer_3=QCform.WriteMCquestion_5.answer3.data, ans_choice_3=QCform.WriteMCquestion_5.ans_multi_select_3.data,
            answer_4=QCform.WriteMCquestion_5.answer4.data, ans_choice_4=QCform.WriteMCquestion_5.ans_multi_select_4.data,
            marks=QCform.WriteMCquestion_5.marks.data,
            topic_tag = '',
            feedback=QCform.WriteMCquestion_5.feedback.data,
            question_type = 'Multiplechoice'
            )
            db.session.add(Q5multi)
            db.session.commit()
            question_5 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_5)
        if QCform.WriteFTGquestion_5.question.data !='':
            Q5FTG = Multiplechoice(
            user_id = current_user.id,
            question = QCform.WriteFTGquestion_5.question.data, 
            answer_1 = QCform.WriteFTGquestion_5.answer.data,
            answer_2 = '',
            answer_3 = '',
            answer_4 = '',
            topic_tag = '',
            marks = QCform.WriteFTGquestion_5.marks.data, 
            feedback = QCform.WriteFTGquestion_5.feedback.data,
            question_type = "fill_in_the_blank"
            )
            db.session.add(Q5FTG)
            db.session.commit()
            question_5 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_5)  
        
        db.session.commit()
        flash('test added')
        return redirect('/Formative_test_list')


    return render_template('create_form_test.html', title = 'Create Formative Assesment', QCform=QCform, test=test)

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
        test_rating = 10,
        test_weighting = 10,
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
    q1answers = Q1TakeFormTestForm()
    q2answers = Q2TakeFormTestForm()
    q3answers = Q3TakeFormTestForm()
    q4answers = Q4TakeFormTestForm()
    q5answers = Q5TakeFormTestForm()
    finish = FinishFormTestForm()
    question_1 = questions[0]
    question_2 = questions[1]
    question_3 = questions[2]
    question_4 = questions[3]
    question_5 = questions[4]

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
            if question_4.answer_1 != q4answers.q3_ans_FTG.data:
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
        if question_1.question != '':
            list.append(lastres.Q1_mark)
        if question_2.question != '':
            list.append(lastres.Q2_mark)
        if question_3.question != '':
            list.append(lastres.Q3_mark)
        if question_4.question != '':
            list.append(lastres.Q4_mark)
        if question_5.question != '':
            list.append(lastres.Q5_mark)
        listtotal = sum(list)
        total_mark_sum = listtotal / len(list)
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
  return redirect('/Formative_test_list.html')
