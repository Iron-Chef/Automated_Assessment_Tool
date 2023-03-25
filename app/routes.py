from flask import render_template, flash, redirect, url_for, request, g,session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User, Multiplechoice, Formativetest, Module
from app.forms import LoginForm, QuestionForm, QChoiceForm, TestChoice
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

@app.route('/choose_create_test', methods=['GET', 'POST'])
@login_required
def choose_create_test():
    form = TestChoice()
    form.question_module.choices = [(module.code, module.name) for module in Module.query.all()]
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
        if QCform.question_2.data != '-':
            question_2 = QCform.question_2.data
            test.linkedquestions.append(question_2) 
        if QCform.question_3.data != '-':
            question_3 = QCform.question_3.data
            test.linkedquestions.append(question_3) 
        if QCform.question_4.data != '-':
            question_4 = QCform.question_4.data
            test.linkedquestions.append(question_4) 
        if QCform.question_5.data != '-':
            question_5 = QCform.question_5.data
            test.linkedquestions.append(question_5) 
        
            db.session.commit()
            flash('Your test is added!')
            return redirect('/create_form_test')


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


