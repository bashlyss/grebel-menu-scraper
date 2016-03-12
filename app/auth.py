from flask.ext.login import LoginManager

from app import app
from app.models import User

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def next_is_valid(path):
    # users should not have access to run the update script
    return not path or 'update' not in path
