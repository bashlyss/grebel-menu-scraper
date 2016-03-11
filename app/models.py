from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))

    def __repr__(self):
       return "<User: {0} {1}>".format(self.id, self.email)

class FoodPreference(db.Model):
    __tablename__ = 'food_preference'

    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", back_populates="preferences")

    def __repr__(self):
       return "<FoodPreference: {0} {1}>".format(self.id, self.food)
