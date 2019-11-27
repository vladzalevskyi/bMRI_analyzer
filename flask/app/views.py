import os
from ast import literal_eval
from flask import render_template, redirect, url_for, request

from app import app
from app.forms import LoginForm, SignUpForm

from app.db_classes import db, Therapists, Patients, Images, ImageAnalysis, ImageTypes, TumorTypes

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=('GET', 'POST'))
def login():
    form = LoginForm()

    #for both POST and valid requests of our form
    if form.validate_on_submit():
        #make request to db and if valid data
        #should redirect for a loged_in page
        #else to the same page but show error
        #use jinja templete and pass a flag, if true
        #display error
        
        #checks if given to form data is in db; return list of found items
        #[]==None
        user = Therapists.query.filter_by(username=form.username.data, password=form.password.data).all()
        if user:
            #redirect to home page
            print("*"*100)
            print(user)
            print("*"*100)

            return redirect(url_for("home", user=user[0]))

        return redirect(url_for('index'))

    return render_template("login.html", form=form) 


@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")


@app.route("/home")
def home():
    user = literal_eval(request.args['user'])
    img_to_review = 2    
    return render_template("home.html", fname=user["first_name"], lname=user["last_name"], img_to_review=img_to_review)



@app.route("/sign_up", methods=('GET', 'POST'))
def sign_up():
    form = SignUpForm()

    if form.validate_on_submit():
        
        #wrap in tre/except
        new_therapist = Therapists(first_name=form.fname.data, last_name=form.lname.data, username=form.username.data, password=form.password.data, title=form.title.data)
        db.session.add(new_therapist)
        db.session.commit()
        return redirect(url_for("index"))
    
    return render_template("sign_up.html", form=form)

"""

@app.route("/test")
def test():
    print(Therapists.query.all())
    return str(Therapists.query.first())
"""