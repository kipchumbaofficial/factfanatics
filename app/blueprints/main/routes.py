#!/usr/bin/env python3
''' routes:
Module for all the routes under main blueprint
'''
import random
from flask import render_template, session, redirect, url_for, flash
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


@main_bp.route('/questions/<category>', methods=['GET', 'POST'])
def questions(category):
    """Fetch random questions for the selected category and manage quiz flow."""
    form = AnswerForm()

    # Fetch the category by name
    current_category = Category.query.filter_by(name=category).first()
    if not current_category:
        flash("Category not found.", "error")
        return redirect(url_for('main.index'))

    # Initialize session for a new category if not already present
    if category not in session.get('questions', {}):
        # Fetch question IDs for the current category
        category_ids = [current_category.id] + [sub.id for sub in current_category.subcategories]
        question_ids_query = db.session.query(CategoryQuestion.question_id).filter(
            CategoryQuestion.category_id.in_(category_ids)
        )
        question_ids = [q[0] for q in question_ids_query.all()]

        # Randomly sample 5 questions
        if len(question_ids) > 5:
            question_ids = random.sample(question_ids, 5)

        # Add new category to the session
        session.setdefault('questions', {})[category] = {
            'question_ids': question_ids,
            'answers': []
        }
        session['current_category'] = category
        session['current_index'] = 0

    # Retrieve session data for the current category
    current_index = session['current_index']
    question_data = session['questions'][category]
    question_ids = question_data['question_ids']

    question_data['id'] = current_category.id

    # Check if quiz for the category is complete
    if current_index >= len(question_ids):
        # Redirect to subcategories or score page
        subcategories = current_category.subcategories
        if subcategories:
            return redirect(url_for('main.sub_categories', category_id=current_category.id))
        else:
            return redirect(url_for('main.result'))

    # Fetch the current question
    current_question_id = question_ids[current_index]
    current_question = Question.query.get(current_question_id)
    if not current_question:
        flash("Question not found.", "error")
        return redirect(url_for('main.index'))

    # Process submitted answer
    if form.validate_on_submit():
        submitted_answer = form.answer.data
        question_data['answers'].append({
            'question_id': current_question_id,
            'answer': submitted_answer
        })
        session['current_index'] += 1
        print(session['questions'])
        return redirect(url_for('main.questions', category=category))

    # Render the current question
    return render_template(
        'question.html',
        question=current_question,
        current_number=current_index + 1,
        total_questions=len(question_ids),
        form=form,
        category=current_category
    )


@main_bp.route('/score', methods=['GET', 'POST'])
@login_required
def result():
    """Process and display quiz results or fetch the latest score if no session data exists."""

    # Handle case where no questions are in session
    if 'questions' not in session:
        latest_score = Score.query.filter_by(user_id=current_user.id).order_by(Score.id.desc()).first()
        scores = Score.query.order_by(Score.score.desc()).all()
        rank = next((i + 1 for i, s in enumerate(scores) if s.user_id == current_user.id), None)
        if latest_score:
            return render_template(
                'result.html',
                score=latest_score.score,
                total_questions=latest_score.total_questions,
                username=current_user.username,
                rank=rank  # Rank might not be relevant here
            )
        else:
            flash("No quiz data found and no previous scores available. Please start a quiz.", "error")
            return redirect(url_for('main.home'))

    # Process quiz results
    total_score = 0
    total_questions = 0
    user_answers = []
    category_id = None  # Default category_id

    for category, data in session['questions'].items():
        question_ids = data['question_ids']
        answers = data['answers']
        category_id = data.get('id')
        print(category_id)

        for answer in answers:
            question_id = answer['question_id']
            user_answer = answer['answer']
            question = Question.query.get(question_id)

            if question:
                is_correct = question.answer.strip().lower() == user_answer.strip().lower()
                if is_correct:
                    total_score += 1

                user_answers.append(UserAnswer(
                    user_id=current_user.id,
                    question_id=question_id,
                    user_answer=user_answer,
                    is_correct=is_correct
                ))
            total_questions += 1

    # Save all answers to the database
    db.session.bulk_save_objects(user_answers)
    db.session.commit()

    # Save the user's total score
    user_score = Score(
        user_id=current_user.id,
        category_id=category_id,  # Ensure category_id is passed
        score=total_score / total_questions,
        total_questions=total_questions
    )
    db.session.add(user_score)
    db.session.commit()

    # Calculate rank
    scores = Score.query.order_by(Score.score.desc()).all()
    rank = next((i + 1 for i, s in enumerate(scores) if s.user_id == current_user.id), None)

    # Clear session
    session.pop('questions', None)
    session.pop('current_category', None)
    session.pop('current_index', None)

    return render_template(
        'result.html',
        score=total_score,
        total_questions=total_questions,
        username=current_user.username,
        rank=rank  # Pass the rank to the template
    )


@main_bp.route('/result', methods=['GET'])
@login_required
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
    .limit(15)\
    .all()

    # Render template
    return render_template('answers.html', user_answers=user_answers)


@main_bp.route('/subcategories/<int:category_id>', methods=['GET'])
def sub_categories(category_id):
    """Selecting Subcategories for a Given Category"""
    # Fetch the category by ID
    category = Category.query.get(category_id)

    if not category:
        # Handle invalid category IDs gracefully
        flash("Category not found.", "error")
        return redirect(url_for('main.home'))

    if not category.subcategories:
        # Redirect to the results page when no subcategories exist
        return redirect(url_for('main.result'))

    # Render the subcategories for the current category
    return render_template(
        'sub-categories.html',
        category=category,
        subcategories=category.subcategories
    )
