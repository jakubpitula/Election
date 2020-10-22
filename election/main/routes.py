from flask import Blueprint, render_template
from election.models import User

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    users = User.query.all()
    return render_template('home.html', users=users)
