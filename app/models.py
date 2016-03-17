from flask.ext.login import UserMixin

from app import sa

class User(sa.Model, UserMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(80))
    email = sa.Column(sa.String(80), unique=True)
    google_id = sa.Column(sa.String(25), unique=True, nullable=True)

    preferences = sa.relationship("FoodPreference", backref="user")

    def __init__(self, name, email, **kwargs):
        super(User, self).__init__(**kwargs)
        self.name = name
        self.email = email

    def __repr__(self):
        return "<User: {0} {1}>".format(self.id, self.email)

class FoodPreference(sa.Model):
    __tablename__ = 'food_preference'

    id = sa.Column(sa.Integer, primary_key=True)
    food = sa.Column(sa.String(80))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    def __repr__(self):
        return "<FoodPreference: {0} {1}>".format(self.id, self.food)
