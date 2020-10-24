from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class CreateForm(FlaskForm):
    first_name = StringField('Imię', validators=[DataRequired()])
    surname = StringField('Nazwisko', validators=[DataRequired()])
    submit = SubmitField('Dodaj')


class UpdateForm(FlaskForm):
    first_name = StringField('Imię', validators=[DataRequired()])
    surname = StringField('Nazwisko', validators=[DataRequired()])
    votes = IntegerField('Głosy', validators=[DataRequired()])
    submit = SubmitField('Edytuj')
