from flask import Blueprint, render_template, flash, redirect, url_for
from election.models import Candidate
from flask_login import login_required, current_user
from election.main.forms import VoteForm
from election import db

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')


@main.route('/voted')
def voted():
    return render_template('home.html')


@main.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    user = current_user
    candidates = Candidate.query.all()
    form = VoteForm()

    choices = []
    for candidate in candidates:
        choices.append((candidate.id, candidate.first_name + ' ' + candidate.surname))

    form.candidate.choices = choices
    if user.voted:
        flash('Nie możesz zagłosować więcej niż jeden raz.', 'danger')
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user.voted = True
        ejected = Candidate.query.get(form.candidate.data)
        ejected.votes += 1
        db.session.commit()
        return redirect(url_for('main.voted'))
    return render_template('vote.html', form=form, title='Głosowanie')
