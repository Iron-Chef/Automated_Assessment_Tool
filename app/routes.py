from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqalchemy import *
from app.models import User, Multiplechoice, Formativetest, Module, Results_sum, Studentanswer
from app.forms import LoginForm, QuestionForm, QChoiceForm, TestChoice, DIFFICULTY_RATING, CreateTestForm, SubmitAttemptForm, StudentAnswerForm, ResultsForm, FillInTheBlankQuestionForm
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

@app.route('/modules', methods=['GET'])
def modules():
    modules = Module.query.all()
    return render_template('modules.html',title='MSc Computing Modules',modules=modules)

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
            flash('this is not yet possible')
            return redirect('/create_form_test') 
    return render_template('choose_create_test.html', title = 'Create New Assesment', form=form)

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


@app.route("/Formative_test_list", methods=['GET'])
def formtests():
    allFormtests = Formativetest.query.all()
    return render_template('Formative_test_list.html', title = 'Formative tests list', allFormtests=allFormtests)

@app.route("/Formative_test/<int:Form_test_id>", methods=['GET'])
def formtest(Form_test_id):
    formtest = Formativetest.query.get_or_404(Form_test_id)
    formtestquestions = formtest.linkedquestions
    return render_template('Formative_test.html', title = formtest.testtitle , formtest=formtest, formtestquestions=formtestquestions)

@app.route("/Formative_test/<int:Form_test_id>/delete", methods=['POST'])
@login_required
def delete_test(Form_test_id):
  test = Formativetest.query.get_or_404(Form_test_id)
  db.session.delete(test)
  db.session.commit()
  flash('Your Post has been deleted')
  return redirect('/Formative_test_list.html')



@app.route("/Formative_test_list", methods=['GET'])
def formtests():
    allFormtests = Formativetest.query.all()
    return render_template('Formative_test_list.html', title = 'Formative tests list', allFormtests=allFormtests)


@app.route("/Formative_test_list/<int:Form_test_id>/delete", methods=['POST'])
@login_required
def delete_test(Form_test_id):
  test = Formativetest.query.get_or_404(Form_test_id)
  db.session.delete(test)
  db.session.commit()
  flash('Your Post has been deleted')
  return redirect('/Formative_test_list.html')
