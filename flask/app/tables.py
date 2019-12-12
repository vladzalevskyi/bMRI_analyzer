from flask_table import Table, Col, LinkCol, ButtonCol, BoolCol
from flask import Markup, url_for
from app.db_classes import Therapists, Patients, ImageTypes, TumorTypes


class TherpistCol(Col):
    #therap_names = [fname + " " + lname for _,fname, lname in Patients.query.join(Therapists, Patients.therapist_id==Therapists.id).add_columns(Therapists.last_name, Therapists.first_name).all()]
    def td_format(self, content):
        therap_names = {t.id:t.first_name + " " + t.last_name for t in Therapists.query.all()}
        return therap_names[content]

# Define a table, then pass in the database records
class PatientsTable(Table):
    pid = Col("Patient's id")
    fullname = Col("Full Name")
    #first_name = Col('First Name')
    #last_name = Col('Last Name')
    ssn = Col('SSN')
    gender = Col("Geder")
    age = Col('Age')

    delete = ButtonCol("Delete", endpoint="patients" ,url_kwargs=dict(delete_id='pid'), allow_sort=False)

    allow_sort= True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('patients', sort=col_key, direction=direction)


class PatientCol(Col):
    #therap_names = [fname + " " + lname for _,fname, lname in Patients.query.join(Therapists, Patients.therapist_id==Therapists.id).add_columns(Therapists.last_name, Therapists.first_name).all()]
    def td_format(self, content):
        patient = {t.pid:str(t.first_name) + " " + str(t.last_name) for t in Patients.query.all()}
        return patient[content]


class ImTypeCol(Col):
    #therap_names = [fname + " " + lname for _,fname, lname in Patients.query.join(Therapists, Patients.therapist_id==Therapists.id).add_columns(Therapists.last_name, Therapists.first_name).all()]
    def td_format(self, content):
        image = {t.id:t.name for t in ImageTypes.query.all()}
        return image[content]

class Diagnosis(Col):
    #therap_names = [fname + " " + lname for _,fname, lname in Patients.query.join(Therapists, Patients.therapist_id==Therapists.id).add_columns(Therapists.last_name, Therapists.first_name).all()]
    def td_format(self, content):
        tumors = {t.id:t.name for t in TumorTypes.query.all()}
        return tumors[content]


class ImagesTable(Table):
    image_id = Col("Image id")
    patient_id = PatientCol('Patient')
    datetime = Col('Datetime')
    im_type = ImTypeCol("Image Type")
    image = LinkCol("Image Location", endpoint="images", url_kwargs=dict(image_url='image'), attr='image')
    delete = ButtonCol("Delete", endpoint="images" ,url_kwargs=dict(delete_id='image_id'), allow_sort=False)
    re_analyze = ButtonCol("Re analyze image", endpoint="images" ,url_kwargs=dict(analyze_id='image_id'), allow_sort=False)
    allow_sort= True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('images', sort=col_key, direction=direction)


class ImageAnalysisTable(Table):
    image_id = LinkCol("Image id", endpoint="image_analysis", url_kwargs=dict(image_url='image_id'), attr='image_id')
    segment = LinkCol("Segmentation", endpoint="image_analysis", url_kwargs=dict(image_url='segment'), attr='image_id')
    tumor = Col('Tumor Analysis')
    diagnosis = Diagnosis("Tumor Type")
    confidence = Col("Confidence") #LinkCol("Image Location", endpoint="images", url_kwargs=dict(image_url='image'), attr='image')
    dt = Col('Datetime')
    recommendations = Col("Recommendations")

    verified = BoolCol("Verified")
    change = ButtonCol("Change Image analysis", endpoint="edit_analysis" ,url_kwargs=dict(image_url='image_id'))
    delete = ButtonCol("Delete", endpoint="image_analysis" ,url_kwargs=dict(delete_id='image_id'), allow_sort=False)

    allow_sort= True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('image_analysis', sort=col_key, direction=direction)
