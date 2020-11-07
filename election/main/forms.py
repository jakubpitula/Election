from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired
from election.models import Candidate


# def get_choices():
#     candidates = Candidate.query.all()
#     choices = []
#     for candidate in candidates:
#         choices.append(candidate.first_name + ' ' + candidate.surname)
#     return choices


class VoteForm(FlaskForm):

    candidate = RadioField('Wybierz jednego z kandydatów.', validators=[DataRequired(message='Musisz wybrać kandydata.')])
    submit = SubmitField('Zagłosuj')
