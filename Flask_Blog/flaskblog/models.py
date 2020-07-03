from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Patient', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.email}')"



class Patient(db.Model, UserMixin):
    patient_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    patient_age = db.Column(db.Integer)
    date_posted = db.Column(db.String(120), unique=True, nullable=False)
    type_of_bed = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), unique=True, nullable=False)
    state=db.Column(db.String(120), unique=True, nullable=False)
    city = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    posts1= db.relationship('Pharmcy', backref='patient', lazy=True)

    def __repr__(self):
        return f"Patient('{self.username}', '{self.patient_age}', '{self.date_posted}', '{self.type_of_bed}', '{self.address}', '{self.state}', '{self.city}', '{self.user_id}')"


class Pharmcy(db.Model, UserMixin):
    medicine_id= db.Column(db.Integer,primary_key=True)
    medicine = db.Column(db.String(20), unique=True, nullable=False)
    quantity = db.Column(db.Integer)
    rate = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    pharmcy_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    posts1= db.relationship('Diagnostics', backref='pharmcy', lazy=True)

    def __repr__(self):
        return f"Pharmcy('{self.medicine}','{self.quantity}','{self.rate}','{self.amount}','{self.pharmcy_id}')"

class Diagnostics(db.Model, UserMixin):
    test_id= db.Column(db.Integer,primary_key=True)
    name_of_test = db.Column(db.String(20), unique=True, nullable=False)
    amount_of_test = db.Column(db.Integer)
    Diagnostic_id = db.Column(db.Integer, db.ForeignKey('pharmcy.pharmcy_id'), nullable=False)

    def __repr__(self):
        return f"Diagnostics('{self.name_of_test}','{self.amount_of_test}','{self.Diagnostic_id}')"