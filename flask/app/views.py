import os
from ast import literal_eval
from datetime import datetime

from sqlalchemy import func
from flask_login import current_user, login_user, logout_user
from flask import render_template, redirect, url_for, request, flash


from app import app
from app.forms import LoginForm, SignUpForm, AddPatientForm
from app.auth import login_manager, load_user, logout_user, login_required, login_user, current_user

from app.db_classes import db, Therapists, Patients, Images, ImageAnalysis, ImageTypes, TumorTypes


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=('GET', 'POST'))
def login():
    # Bypass Login screen if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))


    form = LoginForm()

    #for both POST and valid requests of our form
    if form.validate_on_submit():
        #               **TO DO**
        #make request to db and if valid data
        #should redirect for a loged_in page
        #else to the same page but show error
        #use jinja templete and pass a flag, if true
        #display error
        
        #checks if given to form data is in db; return list of found items
        #[]==None

        # check for username validity == unique field

        user = Therapists.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")

        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("home")

        return redirect(next_page)

    return render_template('login.html', form=form)



@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")

@app.route("/home")
@login_required
def home():
    if not current_user.is_authenticated:
        user = literal_eval(request.args['user'])
    img_to_review = Images.query.join(ImageAnalysis, Images.image_id==ImageAnalysis.image_id).filter_by(verified=False).all()#.add_columns(users.userId, users.name, users.email, friends.userId, friendId).filter(users.id == friendships.friend_id).filter(friendships.user_id == userID).paginate(page, 1, False)
    #img_to_review = db.engine.execute("SELECT * FROM images").fetchall()
    img_today = Images.query.filter(func.DATE(Images.datetime)==datetime.today().date()).all()
    img_analyzed = ImageAnalysis.query.filter(func.DATE(ImageAnalysis.dt)==datetime.today().date()).all()
    return render_template("home.html", user=current_user, img_to_review=len(img_to_review), img_today=len(img_today), img_analyzed=len(img_analyzed))



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/sign_up", methods=('GET', 'POST'))
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = SignUpForm()

    if form.validate_on_submit():
        
        #wrap in tre/except
        new_therapist = Therapists(first_name=form.fname.data, last_name=form.lname.data, username=form.username.data, password=form.password.data, title=form.title.data)
        new_therapist.set_password(form.password.data)
        db.session.add(new_therapist)
        db.session.commit()
        return redirect(url_for("login"))
    
    return render_template("sign_up.html", form=form)


@app.route("/add_patient", methods=('GET', "POST"))
def add_patient():
    available_therapists_id, available_therapists_names = [t.id for t in Therapists.query.all()], [t.first_name + " " + t.last_name for t in Therapists.query.all()]
    
    form = AddPatientForm()
    form.therapist_id.choices = list(zip(available_therapists_id, available_therapists_names))

    if form.validate_on_submit():
        p = Patients.query.first()
        patient = Patients(first_name=form.fname.data, last_name=form.lname.data, gender=form.gender.data, ssn=form.ssn.data, age=form.age.data, therapist_id=form.therapist_id.data)
        db.session.add(patient)
        db.session.commit()
        flash("New patient successfully added")

        return render_template("add_patient.html", form=form)
    return render_template("add_patient.html", form=form)
    #return render_template("add_patient.html", form=form)




"""

@app.route("/test")
def test():
    print(Therapists.query.all())
    return str(Therapists.query.first())
"""