from app import db, login
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

    def __repr__(self):
        return "Student ID: {}, First name: {}, Surnam: {}, Email: {}, Year: {}".format(self.id, self.forename, self.surname, self.email, self.year)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Test(db.Model):
    test_id=db.Column(db.Integer,primary_key=True)
    creator_id= db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    test_type = db.Column(db.Integer, nullable = False)# 0=formative;1=summative
    question_id_1=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)
    question_id_2=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)
    question_id_3=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)
    question_id_4=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)
    question_id_5=db.Column(db.Integer,db.ForeignKey('multiplechoice.id'), nullable=True)


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
    #add difficulty column
    #add tag column
    #add student answer foreignkey
    marks=db.Column(db.Integer, default=False)
    feedback = db.Column(db.Text, default="")
   

    def __repr__(self):
        
        return '{}'.format(self.id)

class Results_sum(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Text, db.ForeignKey('user.id'))
    username = db.Column(db.String(15))
    forename = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    test_id = db.Column(db.Integer)
    mark = db.Column(db.Integer)

    def __repr__(self):
        return f"Results_sum('{self.user_id}','{self.username}', '{self.forename}', '{self.surname}', '{self.test_id}','{self.mark}')"
    



