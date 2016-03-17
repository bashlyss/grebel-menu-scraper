from app.models import User
from app import sa

def get_user_by_google(google_id):
    return User.query.filter(User.google_id == google_id) \
        .one_or_none()

def get_user_by_email(email):
    return User.query.filter(User.email == email) \
        .one_or_none()

def add_user(**kwargs):
    user = User(**kwargs)
    sa.session.add(user)
    sa.session.commit()
    return user
