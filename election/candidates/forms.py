from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, InputRequired


class CreateForm(FlaskForm):
    first_name = StringField('Imię', validators=[DataRequired()])
    surname = StringField('Nazwisko', validators=[DataRequired()])
    submit = SubmitField('Dodaj')


class UpdateForm(FlaskForm):
    first_name = StringField('Imię', validators=[DataRequired()])
    surname = StringField('Nazwisko', validators=[DataRequired()])
    votes = IntegerField('Głosy', validators=[InputRequired()])
    submit = SubmitField('Edytuj')
