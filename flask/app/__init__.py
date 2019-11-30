from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)


app.config['SECRET_KEY'] = 'Hoooray!'
LOCAL_IP = "10.35.2.26"
GLOBAL_IP = "zanner.org.ua"
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://ka7605:123456@{LOCAL_IP}:33321/coursework_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login = LoginManager(app)
login.login_view = 'login'




#should be the last line
from app import views