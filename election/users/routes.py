from flask import Blueprint, flash, request, redirect, render_template, url_for
from election.users.forms import LoginForm, RegistrationForm, UpdateForm
from flask_login import login_user, current_user, logout_user, login_required
from election.models import User
from election import bcrypt, db
from election.utils import admin_required
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import join, dirname, realpath
import random
import string
import smtplib
import os

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
    user = User.query.filter_by(id=id).first_or_404()

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
    user = User.query.filter_by(id=id).first_or_404()
    if not user:
        flash('Użytkownik nieznaleziony', 'danger')
        return redirect(url_for('users.index'))
    db.session.delete(user)
    db.session.commit()
    flash('Użytkownik usunięty', 'success')
    return redirect(url_for('users.index'))


@users.route('/', methods=['GET', 'POST'])
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.vote'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.vote'))
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


def get_randoms(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


def send_emails(mails, logins, passwords, s):
    for email, login, password in zip(mails, logins, passwords):
        msg = MIMEMultipart()
        msg['From'] = os.environ.get('SENDER_MAIL')
        msg['To'] = email
        msg['Subject'] = 'Wybory SzRU 2020 - dane do logowania'
        msg.attach(MIMEText('Wykorzystaj poniższy login i hasło, aby zagłosować w wyborach SzRU.\n'
                            f'Login: {login}\n'
                            f'Hasło: {password}'))
        s.send_message(msg)
        del msg


@users.route('/users/add', methods=['GET'])
@login_required
@admin_required
def add():
    s = smtplib.SMTP(host=os.environ.get('MAIL_HOST'), port=os.environ.get('MAIL_PORT'))
    s.starttls()
    s.login(os.environ.get('SENDER_MAIL'), os.environ.get('SENDER_PASSWORD'))

    path = join(dirname(realpath(__file__)))

    with open(path + '/list.txt') as f:
        mails = [line.strip() for line in f]

    logins, passwords = [], []
    for i in range(len(mails)):
        login = get_randoms(8)
        while login in logins:
            login = get_randoms(8)
        logins.append(login)

        password = get_randoms(12)
        while password in passwords:
            password = get_randoms(12)
        passwords.append(password)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=login, password=hashed_password, admin=False, voted=False)
        db.session.add(user)
    db.session.commit()

    send_emails(mails, logins, passwords, s)

    flash('Dodano użytkowników', 'success')
    return redirect(url_for('users.index'))


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))
