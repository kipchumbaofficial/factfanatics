#!/usr/bin/env python3
""" Contains all the forms used in the user section
"""
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class AnswerForm(FlaskForm):
    '''AnswerForm:
    For users to enter the answer
    '''
    answer = TextAreaField('Answer', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Add category')