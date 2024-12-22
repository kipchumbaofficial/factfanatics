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
    name = db.Column(db.String(50), unique='True', nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    # Relationships
    parent = db.relationship('Category', remote_side=[id], back_populates='subcategories')
    subcategories = db.relationship('Category', back_populates='parent')
    category_questions = db.relationship('CategoryQuestion', back_populates='category')
    scores = db.relationship('Score', back_populates='category')


# Questions Table
class Question(db.Model):
    '''Question:
    Represents questions in the database
    '''
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False )
    answer = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(20), default='easy', nullable=False)
    source = db.Column(db.String(50), nullable=False)
    link = db.Column(db.Text, nullable=False)

    # Relationship
    category_questions = db.relationship('CategoryQuestion', back_populates='questions')
    user_answers = db.relationship('UserAswer', back_populates='question')


# CategoryQuestion Table
class CategoryQuestion(db.Model):
    '''Associative Table for category and questions
    '''
    __tablename__ = 'category_questions'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    questions_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    category = db.relationship('Category', back_populates='category_questions')
    question = db.relationship('Question', back_populates='category_questions')


# Comments Table
class Comment(db.Model):
    '''Comment:
    Represents a comment entity in the database
    '''
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    threshold = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)

    user_comments = db.relationship('UserComment', back_populates='comment')
