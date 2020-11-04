from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from election.models import User


class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zarejestruj się')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


class UpdateForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    password = PasswordField('Hasło')
    voted = BooleanField('Zagłosowano')
    admin = BooleanField('Admin')
    submit = SubmitField('Edytuj')