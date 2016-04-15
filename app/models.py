from flask.ext.login import UserMixin
from pbkdf2 import crypt

from app import sa

class User(sa.Model, UserMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(80))
    email = sa.Column(sa.String(80), unique=True)
    google_id = sa.Column(sa.String(25), unique=True, nullable=True)

    pw_hash = sa.Column(sa.String(100))

    preferences = sa.relationship("FoodPreference", backref="user")

    subscribed = sa.Column(sa.Boolean, default=True)

    def __init__(self, **kwargs):
        # salt is automatically generated when it is unspecified
        pw_hash = crypt(kwargs.pop('password'))
        kwargs['pw_hash'] = pw_hash
        super(User, self).__init__(**kwargs)

    def check_password(self, pw_to_check):
        return self.pw_hash == crypt(pw_to_check, self.pw_hash)

    def __repr__(self):
        return "<User: {0} {1}>".format(self.id, self.email)

class FoodPreference(sa.Model):
    __tablename__ = 'food_preference'

    id = sa.Column(sa.Integer, primary_key=True)
    food = sa.Column(sa.String(80))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    def __repr__(self):
        return "<FoodPreference: {0} {1}>".format(self.id, self.food)
