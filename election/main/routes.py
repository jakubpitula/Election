from flask import Blueprint, render_template, flash, redirect, url_for
from election.models import Candidate
from flask_login import login_required, current_user, logout_user
from election.main.forms import VoteForm
from election import db

main = Blueprint('main', __name__)


@main.route('/home')
def home():
    return render_template('home.html', title='Dzień dobry')


@main.route('/voted')
def voted():
    return render_template('voted.html', title='Dziękujemy')


@main.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    user = current_user
    candidates = Candidate.query.all()
    form = VoteForm()

    choices = []
    values = []
    names = []
    for candidate in candidates:
        choices.append((candidate.id, candidate.first_name + ' ' + candidate.surname))
        values.append(candidate.id)
        names.append(candidate.first_name + ' ' + candidate.surname)

    form.candidate.choices = choices

    if user.voted and not user.admin:
        flash('Nie możesz zagłosować więcej niż jeden raz.', 'danger')
        return redirect(url_for('users.logout'))
    if form.validate_on_submit() and not user.voted:
        user.voted = True
        ejected = Candidate.query.get(form.candidate.data)
        ejected.votes += 1
        db.session.commit()
        logout_user()
        return redirect(url_for('main.voted'))
    return render_template('vote.html', form=form, values=values, names=names, title='Głosowanie')
