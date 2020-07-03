from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User,Patient,Pharmcy,Diagnostics


class RegistrationForm(FlaskForm):
    
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PatientRegistrationForm(FlaskForm):
    
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])            
    patient_age = StringField('Patient Age',
                           validators=[DataRequired()])
    date_posted = StringField('Date',
                           validators=[DataRequired()])
    type_of_bed = StringField('Type of Bed',
                           validators=[DataRequired()])
    address = TextAreaField('Address',
                           validators=[DataRequired()])
    state = StringField('State',
                           validators=[DataRequired()])
    city = StringField('City',
                           validators=[DataRequired()])                                                                    
    submit = SubmitField('Submit')

class UpdatePatient(FlaskForm):
     
    patient_id = StringField('Id',
                           validators=[DataRequired()])            
    
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)]) 
    patient_age = StringField('Patient Age',
                           validators=[DataRequired()])
    date_posted = StringField('Date',
                           validators=[DataRequired()])
    type_of_bed = StringField('Type of Bed',
                           validators=[DataRequired()])
    address = TextAreaField('Address',
                           validators=[DataRequired()])
    state = StringField('State',
                           validators=[DataRequired()])
    city = StringField('City',
                           validators=[DataRequired()])                                                                
    submit = SubmitField('Update')

    def validate_id(self, patient_id):
        user = User.query.filter_by(patient_id=patient_id.data).first()
        if user:
            raise ValidationError('That id is taken. Please choose a different one.')


class SearchPatient(FlaskForm):
     
    patient_id = StringField('Patient Id',
                           validators=[DataRequired()])
    
    submit = SubmitField('Search')

class PharmcyForm(FlaskForm):
    
    medicine = StringField('Medicine',
                           validators=[DataRequired(), Length(min=2, max=20)])            
    quantity = IntegerField('Quantity',
                           validators=[DataRequired()])
    rate = IntegerField('Rate',
                           validators=[DataRequired()])
    amount = IntegerField('Amount',
                           validators=[DataRequired()])
    pharmcy_id = IntegerField('Medicine Id',
                           validators=[DataRequired()])
    submit = SubmitField('Medicine Issues')

class DiagnosticsForm(FlaskForm):
    
    name_of_test = StringField('Medicine',
                           validators=[DataRequired(), Length(min=2, max=20)])            
    amount_of_test = IntegerField('Quantity',
                           validators=[DataRequired()])
    submit = SubmitField('Diagnostics add')
