from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

from app import app

login_manager = LoginManager()

#login_manager.init_app(app)
#login_manager.login_view = ''


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

class User(UserMixin):
  def __init__(self,id):
    self.id = id