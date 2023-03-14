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

    def __repr__(self):
        return "Student ID: {}, First name: {}, Surnam: {}, Email: {}, Year: {}".format(self.student_ID, self.forename, self.surname, self.email, self.year)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


