from flask import render_template, url_for, flash, redirect, request,abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm,PatientRegistrationForm,UpdatePatient,SearchPatient,PharmcyForm,DiagnosticsForm
from flaskblog.models import User,Patient,Pharmcy,Diagnostics
from flask_login import login_user, current_user, logout_user, login_required





@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/patientdetails", methods=['GET', 'POST'])
@login_required
def patientdetails():
    user=User.query.get_or_404(current_user.id)
    patient=Patient.query.filter_by(user_id=user.id).first()
    form = PatientRegistrationForm()
    
    if form.validate_on_submit():
        if patient==None:
            user = Patient(username=form.username.data,patient_age=form.patient_age.data,date_posted=form.date_posted.data,type_of_bed=form.type_of_bed.data,address=form.address.data,state=form.state.data,city=form.city.data,user_id=current_user.id)
            db.session.add(user)
            db.session.commit()
            flash('Your appointment has been booked!', 'success')
            return redirect(url_for('patientdetails'))
        else:
            flash('Your appointment already booked', 'danger')
    
        
    return render_template('patientdetails.html', title='Patient Details',form=form)

@app.route("/updatepatient", methods=['GET', 'POST'])
@login_required
def updatepatient():
    user=User.query.get_or_404(current_user.id)
    patient=Patient.query.filter_by(user_id=user.id).first()
    form = UpdatePatient()
    if patient!=None:
        if form.validate_on_submit():
            
                patient.patient_id=form.patient_id.data
                patient.username=form.username.data
                patient.patient_age=form.patient_age.data
                patient.date_posted=form.date_posted.data
                patient.type_of_bed=form.type_of_bed.data
                patient.address=form.address.data
                patient.state=form.state.data
                patient.city=form.city.data
                db.session.commit()
                flash("Your account has been updated!!!","success")
                return redirect(url_for('updatepatient'))
            
        elif request.method=='GET':
            form.patient_id.data=current_user.id
            
            form.username.data=patient.username
            form.patient_age.data=patient.patient_age
            form.date_posted.data=patient.date_posted
            form.type_of_bed.data=patient.type_of_bed
            form.address.data=patient.address
            form.state.data=patient.state
            form.city.data=patient.city

        return render_template('updatepatient.html', title='Patient Details',form=form)
    else:
        flash("First book your appointment!!!","danger")
        return redirect(url_for('patientdetails'))
        
    
    
@app.route("/deleteappointment",methods=['GET', 'POST'])
@login_required
def deleteappointment():
    form = PatientRegistrationForm()
    user=User.query.get_or_404(current_user.id)
    patient=Patient.query.filter_by(user_id=user.id).first()
    
    if patient!=None: 
        pharmcys=Pharmcy.query.filter_by(pharmcy_id=patient.patient_id).all()
        diagnostics=Diagnostics.query.filter_by(Diagnostic_id=patient.patient_id).all()
        db.session.delete(patient)
        for pharmcy in pharmcys:
            db.session.delete(pharmcy)
        for diagnostic in diagnostics:
            db.session.delete(diagnostic)
        db.session.commit()
        flash('Your appointment has been cancle!!','success')
        return redirect(url_for('patientdetails'))
    else:
        flash('First book your appointment!!','danger')
        return render_template('patientdetails.html', title='Patient Details',form=form)
    
@app.route("/viewpatients")
@login_required
def viewpatients():
    posts=Patient.query.all()
    return render_template('viewpatients.html', title='Patient Details',posts=posts)

@app.route("/searchpatients",methods=['GET', 'POST'])
@login_required
def searchpatients():
    form=SearchPatient()
    patient=Patient.query.filter_by(patient_id=form.patient_id.data).first()
    if form.validate_on_submit():
        if patient!=None:
            flash('Patient Information','success')
            return render_template('searchpatients.html', title='Patient Details',form=form,patient=patient)
        else:
            flash('Patient Not Found!!','danger')
            redirect(url_for('searchpatients',form=form))
            
    return render_template('searchpatients.html', title='Patient Details',form=form)

@app.route("/medicineissues", methods=['GET', 'POST'])
@login_required
def medicineissues():
    user=User.query.get_or_404(current_user.id)
    patient=Patient.query.filter_by(user_id=user.id).first()
    form = PharmcyForm()
    if patient!=None:
        if request.method=="POST":
            phar=Pharmcy(medicine=form.medicine.data,quantity=form.quantity.data,rate=form.rate.data,amount=form.amount.data,pharmcy_id=patient.patient_id)
            db.session.add(phar)
            db.session.commit()
            flash('Medicine Issues', 'success')
            return redirect(url_for('home'))
        
        return render_template('medicineissues.html', title='Medicine Issues', form=form)
    else:
        flash("First book your appointment!!!","danger")
        return redirect(url_for('patientdetails'))

@app.route("/diagnosticsadd", methods=['GET', 'POST'])
@login_required
def diagnosticsadd():
    user=User.query.get_or_404(current_user.id)
    patient=Patient.query.filter_by(user_id=user.id).first()
    form = DiagnosticsForm()
    if patient!=None:
        if request.method=="POST":
            dia=Diagnostics(name_of_test=form.name_of_test.data,amount_of_test=form.amount_of_test.data,Diagnostic_id=patient.patient_id)
            db.session.add(dia)
            db.session.commit()
            flash('Diagnostics added', 'success')
            return redirect(url_for('home'))
        
        return render_template('diagnosticsadd.html', title='Diagnostics add', form=form)
    else:
        flash("First book your appointment!!!","danger")
        return redirect(url_for('patientdetails'))

@app.route("/patientbill")
@login_required
def patientbill():
    user=User.query.get_or_404(current_user.id)
    patients=Patient.query.filter_by(user_id=user.id).first()
    pharmcys=Pharmcy.query.all()
    diagnostics=Diagnostics.query.all()
    sum_pharmcys=0
    sum_diagnostics=0
    if pharmcys!=None and diagnostics!=None:
        for i in pharmcys:
            sum_pharmcys=sum_pharmcys+i.amount
        for i in diagnostics:
            sum_diagnostics=sum_diagnostics+i.amount_of_test
        return render_template('patientbill.html', title='Patient Bill',patients=patients,pharmcys=pharmcys,diagnostics=diagnostics,
        sum_pharmcys=sum_pharmcys,sum_diagnostics=sum_diagnostics)
    else:
        flash("First book your appointment!!!","danger")
        return redirect(url_for('patientbill '))
    
