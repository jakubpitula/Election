from flask_login import UserMixin
from election import login_manager, db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    voted = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"(User: '{self.username}')"


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    votes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"(User: '{self.first_name}', '{self.surname}', '{self.votes}')"
