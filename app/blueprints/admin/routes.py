#!/usr/bin/env python3
'''routes:
Contains all the views of the admin blueprint
'''
from flask import redirect, url_for, render_template, flash
from flask_login import login_required
from app.models.user import User
from app.utils.login_utils import admin_required
from app.forms.admin import CategoryForm, QuestionForm
from app.models.resources import Category, CategoryQuestion, Question
from app.extensions import db
from . import admin_bp


@admin_bp.route('/register', methods=['GET'])
def register():
    """ Log to admin page
    """
    existing_admin = User.query.filter_by(is_admin=True).first()
    if existing_admin:
        return redirect(url_for('main.home'))
    return render_template('admin/register.html')


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    '''dashboard
    Admin dashboard for managing questions and comments
    '''
    category_form = CategoryForm()
    question_form = QuestionForm()

    categories = Category.query.all()
    if categories:
        # Populate choices with existing categories
        category_form.parent_id.choices = [(0, 'None')] + [(c.id, c.name) for c in categories]
        question_form.category_id.choices = [(c.id, c.name) for c in categories]
    else:
        # Only "None" is available when the table is empty
        category_form.parent_id.choices = [(0, 'None')]
        question_form.category_id.choices = []

    return render_template(
        'admin/dashboard.html',
        category_form=category_form,
        question_form=question_form,
        categories=len(categories))


@admin_bp.route('/category/add', methods=['POST'])
@login_required
@admin_required
def add_category():
    '''Handles adding categories to the database'''
    form = CategoryForm()

    # Dynamically set the choices for parent_id
    categories = Category.query.all()
    if categories:
        form.parent_id.choices = [(0, 'None')] + [(c.id, c.name) for c in categories]
    else:
        form.parent_id.choices = [(0, 'None')]

    if form.validate_on_submit():
        # If parent_id is 0, set parent to None
        parent = None if form.parent_id.data == 0 else Category.query.get(form.parent_id.data)
        new_category = Category(name=form.name.data, parent=parent)
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    # Error handling
    flash('An error occurred while adding the category', 'error')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/question/add', methods=['POST'])
@login_required
@admin_required
def add_question():
    '''Handles adding questions to the database'''
    form = QuestionForm()

    # Populate the category_id choices dynamically
    categories = Category.query.all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        new_question = Question(
            question=form.question.data,
            answer=form.answer.data,
            difficulty=form.difficulty.data,
            source=form.source.data,
            link=form.link.data
        )
        db.session.add(new_question)
        db.session.commit()

        # Add the question to the selected category
        category_question = CategoryQuestion(
            category_id=form.category_id.data,
            question_id=new_question.id
        )
        db.session.add(category_question)
        db.session.commit()

        flash('Question added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    flash('An error occurred while adding the question.', 'error')
    return redirect(url_for('admin.dashboard'))
