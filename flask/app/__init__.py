from flask import Flask
from flask_login import LoginManager
import os
app = Flask(__name__)


app.config['SECRET_KEY'] = 'Hoooray!'
LOCAL_IP = "10.35.2.26"
GLOBAL_IP = "zanner.org.ua"

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://ka7605:123456@{GLOBAL_IP}:33321/coursework_db'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.path.abspath(".."), 'uploads') # you'll need to create a folder named uploads

#os.makedirs(app.config['UPLOADED_PHOTOS_DEST'], exist_ok=True)

login = LoginManager(app)
login.login_view = 'login'




#should be the last line
from app import views
