import os

from app import app
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():

    return render_template("login.html")


@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")
