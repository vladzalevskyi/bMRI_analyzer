import os
from ast import literal_eval
from datetime import datetime
import requests
import json

from sqlalchemy import func, desc, asc
from sqlalchemy.orm import load_only
from flask_login import current_user, login_user, logout_user
from flask import render_template, redirect, url_for, request, flash
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class


from app import app
from app.forms import LoginForm, SignUpForm, AddPatientForm, ImageForm
from app.auth import login_manager, load_user, logout_user, login_required, login_user, current_user

from app.db_classes import db, Therapists, Patients, Images, ImageAnalysis, ImageTypes, TumorTypes

from app.tables import PatientsTable, Col, ImagesTable

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB


ML_URL = 'http://0.0.0.0:5002/api/detect'
ITEMS_PER_PAGE = 5


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
        #use jinja templete and pass a flag, if true
        #display error

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
        #p = Patients.query.first()
        patient = Patients(first_name=form.fname.data, last_name=form.lname.data, gender=form.gender.data, ssn=form.ssn.data, age=form.age.data, therapist_id=form.therapist_id.data)
        db.session.add(patient)
        db.session.commit()
        flash("New patient successfully added")

        return render_template("add_patient.html", form=form)
    return render_template("add_patient.html", form=form)
    #return render_template("add_patient.html", form=form)


@app.route("/upload_image",  methods=('GET', "POST"))
def upload_image():

    pid,pnames = [t.pid for t in Patients.query.all()], [str(t.first_name) + " " + str(t.last_name) for t in Patients.query.all()]
    imtypes_id,imtype_names = [t.id for t in ImageTypes.query.all()], [t.name for t in ImageTypes.query.all()]

    form = ImageForm()
    form.patient_id.choices = list(zip(pid, pnames))
    form.im_type.choices = list(zip(imtypes_id, imtype_names))

    if form.validate_on_submit():
        filename = photos.save(form.photo.data, name=f"{form.patient_id.data}_{form.datetime.data}_{current_user.id}.")
        file_url = photos.url(filename)

        img = Images(patient_id=form.patient_id.data, datetime=form.datetime.data, im_type=form.im_type.data, image=filename)
        db.session.add(img)
        db.session.commit()
        flash("New image successfully added")
        if form.analyze.data:
            #send POST request to ml module
            res = requests.post(ML_URL, json={'impath':filename})

            if res.status_code == 200:

                result = json.loads(res.text)
                diagnosis = 1 if result["tumor_detected"]==False else 2
                img_anal = ImageAnalysis(image_id=img.image_id, segment=result["segmentation_img"], tumor=result["classification"], diagnosis=diagnosis, recommendations=None, confidence=result["confidence"], dt=datetime.now(), verified=False)
                
                db.session.add(img_anal)
                db.session.commit()
                
                #flash(img_anal)
                flash("Successfully analyzed new image")
            else:
                flash("Error when analyzing")

    else:
        file_url = None
    return render_template("upload_image.html", form=form, file_url=file_url)


@app.route("/patients",  methods=('GET', "POST"))
def patients():
    sort = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    
    if reverse:
        p = Patients.query.order_by(getattr(Patients, sort).asc()).all()
    else:
        p = Patients.query.order_by(getattr(Patients, sort).desc()).all()
    

    ptable = PatientsTable(p,
                          sort_by=sort,
                          sort_reverse=reverse)
    
    #   ptable = PatientsTable(items=p)
    
    return ptable.__html__()


@app.route("/images",  methods=('GET', "POST"))
def images():
    sort = request.args.get('sort', 'image_id')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    image_url = photos.url(request.args.get("image_url", ""))
    page = request.args.get('page', 1, type=int)
    #add image view

    if reverse:
        iquery = Images.query.order_by(getattr(Images, sort).asc()).paginate(page, ITEMS_PER_PAGE, False)
        i = iquery.items
    else:
        iquery = Images.query.order_by(getattr(Images, sort).desc()).paginate(page, ITEMS_PER_PAGE, False)
        i = iquery.items
    

    next_url = url_for('images', page=iquery.next_num) if iquery.has_next else None
    prev_url = url_for('images', page=iquery.prev_num) if iquery.has_prev else None



    itable = ImagesTable(i,
                          sort_by=sort,
                          sort_reverse=reverse)
    
    #   ptable = PatientsTable(items=p)
    
    return render_template("images.html", table=itable, simage=image_url, next_url=next_url, prev_url=prev_url)