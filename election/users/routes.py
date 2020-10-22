from flask import Blueprint, flash, request, abort, redirect, render_template, url_for
from election.users.forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user ,logout_user
from election.models import User
from election import bcrypt, db
from is_safe_url import is_safe_url

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Zalogowano.', 'success')
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('main.home'))
    return render_template('login.html', form=form)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, admin=False, voted=False)
        db.session.add(user)
        db.session.commit()
        flash('Użytkownik został zarejestrowany.')
        return redirect(url_for('main.home'))
    return render_template('register.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
