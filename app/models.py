from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(10), index = True)
    forename = db.Column(db.String(128), index = True)
    surname = db.Column(db.String(128), index = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    year = db.Column(db.Integer)
    is_lecturer = db.Column(db.Boolean, nullable = False, default = False)
    results_s = db.relationship('Results_sum', backref='user', lazy=True)
    testauthor = db.relationship('Formativetest', backref = 'tstathr', lazy=True)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return "Student ID: {}, First name: {}, Surnam: {}, Email: {}, Year: {}".format(self.id, self.forename, self.surname, self.email, self.year)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Module(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    code=db.Column(db.Text, default="")
    name=db.Column(db.Text, default="")
    credits=db.Column(db.Integer)
    formtestref = db.relationship('Formativetest', backref = 'mdls', lazy=True)

#formtest to questions many-many realtionship table - rj
Mc_Ft = db.Table('Mc_Ft',
    db.Column('Mc_id', db.Integer, db.ForeignKey('multiplechoice.id'), primary_key=True),
    db.Column('Ft_id', db.Integer, db.ForeignKey('formativetest.id'), primary_key=True)    
)

class Test(db.Model):
    test_id=db.Column(db.Integer,primary_key=True)
    creator_id= db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    test_type = db.Column(db.Integer, nullable = False)# 0=formative;1=summative
    question_id_1=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)
    question_id_2=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)
    question_id_3=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)
    question_id_4=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)
    question_id_5=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)
    attempt = db.relationship('FormativeAttempt', backref='test_to_attempt', lazy=True)
    
    
    def __repr__(self):
        return f"Test('{self.test_id}', '{self.creator_id}', '{self.test_type}', '{self.question_id_1}', '{self.question_id_2}', '{self.question_id_3}', '{self.question_id_4}', '{self.question_id_5}')"

#rj
class Formativetest(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    testtitle = db.Column(db.Text,)
    author = db.Column(db.Text, db.ForeignKey('user.id'))
    module_code = db.Column(db.Integer, db.ForeignKey('module.id'))
    linkedquestions = db.relationship('Multiplechoice', secondary = Mc_Ft, backref=db.backref('linkquestions', lazy=True),lazy='subquery')

class Multiplechoice(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id=db.Column(db.Text, db.ForeignKey('user.id'))
    # add foreignkey to summative and formative or vice versa
    question= db.Column(db.Text, default="")
    answer_1= db.Column(db.Text, default="")
    ans_choice_1 = db.Column(db.Integer, default=False)
    answer_2= db.Column(db.Text, default="")
    ans_choice_2 = db.Column(db.Integer, default=False)
    answer_3= db.Column(db.Text, nullable=True)
    ans_choice_3 = db.Column(db.Integer, default=False)
    answer_4= db.Column(db.Text, nullable=True)
    ans_choice_4 = db.Column(db.Integer, default=False)
    rating = db.Column(db.Unicode(40))
    rating_num=db.Column(db.Integer)
    #add tag column
    #add difficulty column
    #add student answer foreignkey
    subject_tag = db.Column(db.Text, default = "")
    marks=db.Column(db.Integer, default=False)
    feedback = db.Column(db.Text, default="")
    topic_tag = db.Column(db.Text, default = "")
    question_type = db.Column(db.Text, nullable = False)
    
    def __repr__(self):

        return "id: {}, Question: {}, Answer 1: {}, Answer 2: {}, Answer 3: {}, Answer 4: {}".format(self.id, self.question, self.answer_1, self.answer_2, self.answer_3, self.answer_4)

class Studentanswer(db.Model):
    
    id=db.Column(db.Integer, primary_key=True)
    question_id=db.Column(db.Integer, db.ForeignKey('multiplechoice.id'),
    nullable=True)#should be False
    user_id = db.Column(db.Text, db.ForeignKey('user.id'))
    ans_choice_1 = db.Column(db.Integer, default=False)
    ans_choice_2  = db.Column(db.Integer, default=False)
    ans_choice_3  = db.Column(db.Integer, default=False)
    ans_choice_4 = db.Column(db.Integer, default=False)

    def get_question(self):
        return Multiplechoice.query.filter_by(question_id=Multiplechoice.id).order_by(Multiplechoice.id.desc())

# SP - resutls table
class Results_sum(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Text, db.ForeignKey('user.id'))
    username = db.Column(db.String(15))
    forename = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    # attempt date
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cohort_year = db.Column(db.String(15))
    # unique test ref
    test_id = db.Column(db.Integer)
    # 0 = formative result, 1 = summative result
    form_summ = db.Column(db.Integer)
    # module result relates to
    res_module = db.Column(db.String(128))
    Q1_mark = db.Column(db.Integer)
    Q1_attempts = db.Column(db.Integer)
    Q2_mark = db.Column(db.Integer)
    Q2_attempts = db.Column(db.Integer)
    Q3_mark = db.Column(db.Integer)
    Q3_attempts = db.Column(db.Integer)
    Q4_mark = db.Column(db.Integer)
    Q4_attempts = db.Column(db.Integer)
    Q5_mark = db.Column(db.Integer)
    Q5_attempts = db.Column(db.Integer)
    # test total mark (%)
    total_mark = db.Column(db.Integer)
    # difficulty (total)
    test_rating = db.Column(db.Integer)
    # test contribution to total module credit
    test_weighting = db.Column(db.Integer)

    def __repr__(self):
        return f"Results_sum('{self.user_id}','{self.username}', '{self.forename}', '{self.surname}', '{self.test_id}','{self.total_mark}','{self.cohort_year}','{self.res_module}' ,'{self.Q1_mark}','{self.Q1_attempts}' ,'{self.Q2_mark}','{self.Q2_attempts}','{self.Q3_mark}','{self.Q3_attempts}','{self.Q4_mark}','{self. Q4_attempts}','{self.Q5_mark}','{self.Q5_attempts}','{self.test_rating}','{self.form_summ}','{self.test_weighting}','{self.date}')"



class FormativeAttempt(db.Model):
    attempt_id=db.Column(db.Integer(),primary_key=True)
    test_id=db.Column(db.Integer(),db.ForeignKey('test.test_id'),nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    question_id_1=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)
    question_id_2=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)
    question_id_3=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)
    question_id_4=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)
    question_id_5=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)
    answer_1=db.Column(db.Integer,nullable=True)
    answer_2=db.Column(db.Integer,nullable=True)
    answer_3=db.Column(db.Integer,nullable=True)
    answer_4=db.Column(db.Integer,nullable=True)
    answer_5=db.Column(db.Integer,nullable=True)
    marks=db.Column(db.Integer,nullable=False)
    
class Result(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    attempt=db.Column(db.Integer,db.ForeignKey('formative_attempt.attempt_id'),nullable=False)
    marks=db.Column(db.Integer)
    
    

    
    
