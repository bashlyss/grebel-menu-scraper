from app.models import User, FoodPreference
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

def get_preference_by_id(pref_id):
    return FoodPreference.query.filter(FoodPreference.id == pref_id).one_or_none()

def delete_preference(preference):
    sa.session.delete(preference)
    sa.session.commit()

def add_preference(**kwargs):
    preference = FoodPreference(**kwargs)
    sa.session.add(preference)
    sa.session.commit()
    return preference

def get_preferences_by_userid(user_id):
    return FoodPreference.query.filter(FoodPreference.user_id == user_id)
