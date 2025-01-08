#!/usr/bin/env python3
''' routes:
Module for all the routes under main blueprint
'''
from flask import render_template, request, session, redirect, url_for, flash
from sqlalchemy import func
from flask_login import login_required, current_user
from app.extensions import db
from app.forms.user import AnswerForm
from app.models.resources import Category, CategoryQuestion, Question
from app.models.user import Score, UserAnswer
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
    form = AnswerForm()

    session['current_category'] = category

    # Check if questions for the quiz are already stored in the session
    if 'question_ids' not in session or session.get('current_category') != category:
        # Fetch root and subcategories
        root = Category.query.filter_by(name=category).first()
        if not root:
            return "Category not found", 404

        all_categories = [root] + root.subcategories
        category_ids = [category.id for category in all_categories]

        # Fetch all question IDs for the category
        question_ids = db.session.query(CategoryQuestion.question_id).filter(
            CategoryQuestion.category_id.in_(category_ids)
        ).order_by(func.random()).limit(5)
        question_ids = [q[0] for q in question_ids]

        # Save question list and current category in the session
        session['question_ids'] = question_ids
        session['current_category'] = category
        session['current_index'] = 0  # Start from the first question

    # Get the current question index
    current_index = session.get('current_index', 0)

    # Check if the index exceeds the number of questions
    question_ids = session['question_ids']
    if current_index >= len(question_ids):
        return redirect(url_for('main.result'))

    # Fetch the current question
    current_question_id = question_ids[current_index]
    current_question = Question.query.get(current_question_id)

    # Pass current question number and total questions
    return render_template(
        'question.html',
        question=current_question,
        current_number=current_index + 1,
        total_questions=len(question_ids),
        form=form
    )


@main_bp.route('/submit-answer', methods=['POST'])
def submit_answer():
    '''Submit answer t be added to session
    '''
    # Get the user's answer and current question
    question_id = request.form.get('question_id')
    user_answer = request.form.get('answer')

    # Optionally, validate and store the answer in the session
    if 'answers' not in session:
        session['answers'] = {}
    session['answers'][question_id] = user_answer

    # Increment the current question index
    session['current_index'] = session.get('current_index', 0) + 1

    # Redirect to the questions route
    category = session.get('current_category')
    if not category:
        return redirect(url_for('main.home'))  # Redirect to home if category is missing
    return redirect(url_for('main.questions', category=category))


@main_bp.route('/score', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in
def result():
    """Handles both quiz result submission and displaying the latest results."""

    score, total_questions, category_name = None, None, None

    if 'answers' in session and 'question_ids' in session and 'current_category' in session:
        # Session data exists, process quiz results
        answers = session.get('answers', {})
        question_ids = session.get('question_ids', [])
        category_name = session.get('current_category')

        # Fetch category
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            flash("Invalid category. Please try again.", "error")
            return redirect(url_for('main.home'))

        # Calculate score
        total_questions = len(question_ids)
        score = 0
        for question_id in question_ids:
            user_answer = answers.get(str(question_id), None)
            question = Question.query.get(question_id)

            if not question:
                continue  # Skip if question is not found

            is_correct = question.answer.lower() == user_answer.lower() if user_answer else False
            if is_correct:
                score += 1

            # Save user answer
            user_answer_entry = UserAnswer(
                user_id=current_user.id,
                question_id=question_id,
                user_answer=user_answer,
                is_correct=is_correct
            )
            db.session.add(user_answer_entry)

        # Save score to the database
        user_score = Score(
            user_id=current_user.id,
            category_id=category.id,
            score=score
        )
        db.session.add(user_score)
        db.session.commit()

        # Clear session data
        session.pop('answers', None)
        session.pop('question_ids', None)
        session.pop('current_category', None)
        session.pop('current_index', None)

    else:
        # No session data, fetch the latest score
        user_score = (
            db.session.query(Score)
            .filter_by(user_id=current_user.id)
            .order_by(Score.id.desc())
            .first()
        )

        if not user_score:
            flash("No quiz results found. Please complete a quiz to see your results.", "warning")
            return redirect(url_for('main.home'))

        # Set variables from the latest score
        score = user_score.score
        total_questions = 5
        category_name = user_score.category.name  # Assuming a relationship with `Category`

    # Calculate rank for the user in the latest category
    rank_query = db.session.query(
    Score.user_id,
    func.rank().over(
        order_by=func.max(Score.score).desc(),
        partition_by=Score.category_id
    ).label('rank')
    ).group_by(Score.user_id, Score.category_id).subquery()

    # Retrieve the rank of the current user
    user_rank = db.session.query(rank_query.c.rank).filter(rank_query.c.user_id == current_user.id).scalar()

    # Render the result page
    return render_template(
        'result.html',
        score=score,
        total_questions=total_questions,
        category=category_name,
        username=current_user.username,
        rank=user_rank
    )


@main_bp.route('/result', methods=['GET'])
def show_result():
    """Result page to show the latest five answers with additional details"""
    # Fetch the latest five user's answers, questions, correctness, source, and link
    user_answers = db.session.query(
        UserAnswer.id,
        Question.question.label('question_text'),
        UserAnswer.user_answer,
        Question.answer.label('correct_answer'),
        UserAnswer.is_correct,
        Question.source,
        Question.link
    ).join(Question, UserAnswer.question_id == Question.id)\
    .filter(UserAnswer.user_id == current_user.id)\
    .order_by(UserAnswer.answered_at.desc())\
    .limit(5)\
    .all()

    # Render template
    return render_template('answers.html', user_answers=user_answers)
