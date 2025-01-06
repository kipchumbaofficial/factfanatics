#!/usr/bin/env python3
''' routes:
Module for all the routes under main blueprint
'''
from flask import render_template, request
from sqlalchemy import func
from app.extensions import db
from app.models.resources import Category, CategoryQuestion, Question
from . import main_bp


@main_bp.route('/')
def home():
    '''Home route
    '''
    return render_template('home.html')


@main_bp.route('/login', methods=['GET'])
def login():
    """ Log in page
    """
    return render_template('login.html')


@main_bp.route('/play')
def categories():
    '''Categories Route
    For users to select categories
    '''
    parent_categories = Category.query.filter_by(parent_id=None).all()
    return render_template(
        'categories.html',
        categories=parent_categories)


@main_bp.route('/questions/<category>')
def questions(category):
    '''Selects questions randomly for user
    '''
    root = Category.query.filter_by(name=category).first()

    # Get root and subcategories
    all_categories = [root] + root.subcategories
    category_ids = [category.id for category in all_categories]

    # Fetch all question IDs for the category
    question_ids = db.session.query(CategoryQuestion.question_id).filter(
        CategoryQuestion.category_id.in_(category_ids)
    ).order_by(func.random()).all()
    question_ids = [q[0] for q in question_ids]

    # Retrieve the current question based on query parameter (default: first question)
    current_index = int(request.args.get('current', 0))
    if current_index >= len(question_ids):
        return 'Congrats'  # Redirect to results page

    current_question_id = question_ids[current_index]
    current_question = Question.query.get(current_question_id)

    # Pass current question number and total questions
    return render_template(
        'question.html',
        question=current_question,
        current_number=current_index + 1,
        total_questions=len(question_ids),
        next_index=current_index + 1
    )
