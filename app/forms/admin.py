#!/usr/bin/env python3
""" Contains all the forms used in the admin section
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, URL


class CategoryForm(FlaskForm):
    '''CategoryForm:
    Adds a category to the database
    '''
    name = StringField('Category Name', validators=[DataRequired(), Length(max=50)])
    parent_id = SelectField('Parent Category', choices=[], coerce=int, default=0)
    submit = SubmitField('Add category')


class QuestionForm(FlaskForm):
    '''Form for adding questions
    '''
    question = TextAreaField('Question Text', validators=[DataRequired(), Length(max=500)])
    answer = StringField('Answer', validators=[DataRequired(), Length(max=255)])
    difficulty = SelectField(
        'Difficulty',
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        default='easy'
    )
    source = StringField('Source', validators=[DataRequired(), Length(max=50)])
    link = URLField('Source Link', validators=[DataRequired(), URL()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Question')
