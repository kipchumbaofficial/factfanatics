#!/usr/bin/env python3
"""resources:
    Contains all the resource classes and functions for the application.
"""
from datetime import datetime
from app.extensions import db


class Category(db.Model):
    '''Category
    Represents question category in the database
    '''
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id'),
        index=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    parent = db.relationship(
        'Category',
        remote_side=[id],
        back_populates='subcategories')
    subcategories = db.relationship(
        'Category',
        back_populates='parent',
        cascade='all, delete-orphan')
    category_questions = db.relationship(
        'CategoryQuestion',
        back_populates='category',
        cascade='all, delete-orphan')
    scores = db.relationship(
        'Score',
        back_populates='category',
        cascade='all, delete-orphan')

    def __repr__(self):
        """
        Returns a string representation of the Category instance.
        """
        return f"<Category('{self.name}')>"


# Questions Table
class Question(db.Model):
    '''Question:
    Represents questions in the database
    '''
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(20), default='easy', nullable=False)
    source = db.Column(db.String(50), nullable=False)
    link = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationship
    category_questions = db.relationship(
        'CategoryQuestion',
        back_populates='questions',
        cascade='all, delete-orphan')
    user_answer = db.relationship(
        'UserAnswer',
        back_populates='question',
        cascade='all, delete-orphan')

    def __repr__(self):
        """
        Returns a string representation of the Question instance.
        """
        return f"<Question('{self.question}')>"


# CategoryQuestion Table
class CategoryQuestion(db.Model):
    '''Associative Table for category and questions
    '''
    __tablename__ = 'category_questions'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id', ondelete='CASCADE'),
        nullable=False,
        index=True)
    question_id = db.Column(
        db.Integer,
        db.ForeignKey('questions.id', ondelete='CASCADE'),
        nullable=False,
        index=True)

    category = db.relationship('Category', back_populates='category_questions')
    questions = db.relationship('Question', back_populates='category_questions')

    def __repr__(self):
        """
        Returns a string representation of the CategoryQuestion instance.
        """
        return (f"<CategoryQuestion(Category ID: {self.category_id}, "
                f"Question ID: {self.question_id})>")


# Comments Table
class Comment(db.Model):
    '''Comment:
    Represents a comment entity in the database
    '''
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    threshold = db.Column(db.Integer, nullable=False, index=True)
    trait = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_comments = db.relationship(
        'UserComment',
        back_populates='comment',
        cascade='all, delete-orphan')

    def __repr__(self):
        """
        Returns a string representation of the Comment instance.
        """
        return f"<Comment('{self.comment[:30]}...')>"
