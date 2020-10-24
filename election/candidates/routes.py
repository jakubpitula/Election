from flask import Blueprint, flash, redirect, render_template, url_for, request
from election.models import Candidate
from election.candidates.forms import CreateForm, UpdateForm
from election import db

candidates = Blueprint('candidates', __name__)


@candidates.route('/candidates/create', methods=['GET', 'POST'])
def create():
    form = CreateForm()
    if form.validate_on_submit():
        candidate = Candidate(first_name=form.first_name.data, surname=form.surname.data, votes=0)
        db.session.add(candidate)
        db.session.commit()
        flash('Kandydat został utworzony.')
        return redirect(url_for('candidates.index'))
    return render_template('candidates/create.html', form=form)


@candidates.route('/candidates', methods=['GET'])
def index():
    all_candidates = Candidate.query.all()
    return render_template('candidates/index.html', candidates=all_candidates)


@candidates.route('/candidates/<id>/update', methods=['GET', 'POST'])
def update(id):
    form = UpdateForm()
    candidate = Candidate.query.get(id)

    if form.validate_on_submit():
        candidate.first_name = form.first_name.data
        candidate.surname = form.surname.data
        candidate.votes = form.votes.data
        db.session.commit()
        flash('Zaktualizowano!', 'success')
        return redirect(url_for('candidates.index'))
    elif request.method == 'GET':
        form.first_name.data = candidate.first_name
        form.surname.data = candidate.surname
        form.votes.data = candidate.votes
    return render_template('candidates/update.html', form=form)


@candidates.route('/candidates/<id>/delete', methods=['GET'])
def delete(id):
    candidate = Candidate.query.get(id)
    if not candidate:
        flash('Kandydat nieznaleziony', 'danger')
        return redirect(url_for('candidates.index'))
    db.session.delete(candidate)
    db.session.commit()
    flash('Kandydat usunięty', 'success')
    return redirect(url_for('candidates.index'))
