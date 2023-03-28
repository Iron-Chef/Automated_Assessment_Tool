from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy import *
from app.models import User,Test, Multiplechoice, FormativeAttempt,Results_sum
from app.forms import LoginForm, CreateTestForm, QuestionForm, SubmitAttemptForm, ResultsForm, FillInTheBlankQuestionForm
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
        feedback=form.feedback.data,
        topic_tag = form.topic.data,
        question_type = "multiple_choice"
        )
        db.session.add(multi)
        db.session.commit()
        flash('Your question is added!')
        return redirect('/question_list')
    return render_template("add_mc_questions.html", title="Add Multiple Choice Questions", form=form)

@app.route("/mc_question/delete/<int:mc_question_id>")
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

@app.route("/mc_question/<int:mc_question_id>", methods=['GET'])
def mcquestion(mc_question_id):
    mcquestion=Multiplechoice.query.get_or_404(mc_question_id)

    return render_template('mc_question.html', mcquestion=mcquestion, title=mcquestion.question, mc_question_id=mcquestion.id)


@app.route("/mc_question/edit/<int:mc_question_id>", methods=['GET', 'POST'])
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
        db.session.add(mcquestion)
        db.session.commit()
        flash("Multiple Choice Question amended")
        return redirect('/question_list')

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
        feedback = form.feedback.data,
        topic_tag = form.topic.data,
        question_type = "fill_in_the_blank"
        )
        db.session.add(question)
        db.session.commit()

        flash('Question added!')
        return redirect('/question_list')

    return render_template('add_fill_in_the_blank_question.html', form = form)

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

# Add code-challenge questions
@app.route("/add_code_challenge_question.html", methods = ['GET', 'POST'])
def add_code_challenge_question():
    return render_template('add_code_challenge_question.html')

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
    elif order_by == "difficulty":
        questions = Multiplechoice.query.order_by(Multiplechoice.difficulty)
    
    return render_template('question_list.html', questions = questions)

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


