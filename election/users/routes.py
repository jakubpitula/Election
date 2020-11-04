from flask import Blueprint, flash, request, abort, redirect, render_template, url_for
from election.users.forms import LoginForm, RegistrationForm, UpdateForm
from flask_login import login_user, current_user, logout_user, login_required
from election.models import User
from election import bcrypt, db
from election.utils import admin_required
from is_safe_url import is_safe_url

users = Blueprint('users', __name__)


@users.route('/users/index', methods=['GET'])
@admin_required
def index():
    all_users = User.query.all()
    return render_template('users/index.html', users=all_users)


@users.route('/users/<id>/update', methods=['GET', 'POST'])
@admin_required
def update(id):
    form = UpdateForm()
    user = User.query.get(id)

    if form.validate_on_submit():
        user.username = form.username.data
        if form.password.data:
            user.password = bcrypt.generate_password_hash(form.password.data)
        user.voted = form.voted.data
        user.admin = form.admin.data
        db.session.commit()
        flash('Zaktualizowano!', 'success')
        return redirect(url_for('users.index'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.admin.data = user.admin
        form.voted.data = user.voted
    return render_template('users/update.html', form=form)


@users.route('/users/<id>/delete', methods=['GET'])
@admin_required
def delete(id):
    user = User.query.get(id)
    if not user:
        flash('Użytkownik nieznaleziony', 'danger')
        return redirect(url_for('users.index'))
    db.session.delete(user)
    db.session.commit()
    flash('Użytkownik usunięty', 'success')
    return redirect(url_for('users.index'))


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.voted'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Zalogowano.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.voted'))
        else:
            flash('Nieprawidłowe dane logowania.', 'danger')
    return render_template('login.html', form=form)


@users.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, admin=False, voted=False)
        db.session.add(user)
        db.session.commit()
        flash('Użytkownik został utworzony.')
        return redirect(url_for('main.voted'))
    return render_template('users/create.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.voted'))
