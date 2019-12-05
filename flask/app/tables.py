from flask_table import Table, Col, LinkCol
from flask import Markup, url_for
from app.db_classes import Therapists, Patients, ImageTypes


class TherpistCol(Col):
    #therap_names = [fname + " " + lname for _,fname, lname in Patients.query.join(Therapists, Patients.therapist_id==Therapists.id).add_columns(Therapists.last_name, Therapists.first_name).all()]
    def td_format(self, content):
        therap_names = {t.id:t.first_name + " " + t.last_name for t in Therapists.query.all()}
        return therap_names[content]

# Define a table, then pass in the database records
class PatientsTable(Table):
    pid = Col("Patient's id")
    last_name = Col('Last Name')
    first_name = Col('First Name')
    ssn = Col('SSN')
    gender = Col("Geder")
    age = Col('Age')
    therapist_id = TherpistCol("Therapist")

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

class ImagesTable(Table):
    image_id = Col("Image id")
    patient_id = PatientCol('Patient')
    datetime = Col('Datetime')
    im_type = ImTypeCol("Image Type")
    image = LinkCol("Image Location", endpoint="images", url_kwargs=dict(image_url='image'), attr='image')

    allow_sort= True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('images', sort=col_key, direction=direction)

