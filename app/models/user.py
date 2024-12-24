#!/usr/bin/env python3
""" User model:
User class
"""
from datetime import datetime
from flask_login import UserMixin
from app.extensions import db


class User(UserMixin, db.Model):
    """ User:
    Represents a user entity in the database.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # Relationships
    scores = db.relationship(
        'Score',
        back_populates='user',
        cascade='all, delete-orphan')
    comments = db.relationship(
        'UserComment',
        back_populates='user',
        cascade='all, delete-orphan')
    answers = db.relationship(
        'UserAnswer',
        back_populates='user',
        cascade='all, delete-orphan')

    def __repr__(self):
        """
        Returns a string representation of the User instance.
        """
        return f"<User('{self.username}', '{self.email}')>"


class Score(db.Model):
    '''Score:
    Represents a score entity in the database
    '''
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False, index=True)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id', ondelete='CASCADE'),
        nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationship
    user = db.relationship('User', back_populates='scores')

    def __repr__(self):
        """
        Returns a string representation of the Score instance.
        """
        return f"<Score('{self.score}')>"


class UserComment(db.Model):
    '''UserComment
    Associative table for users and comments
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False, index=True)
    comment_id = db.Column(
        db.Integer,
        db.ForeignKey('comments.id', ondelete='CASCADE'),
        nullable=False, index=True)

    user = db.relationship('User', back_populates='comments')
    comment = db.relationship('Comment', back_populates='user_comments')

    def __repr__(self):
        """
        Returns a string representation of the UserComment instance.
        """
        return f"<UserComment('{self.comment_id}', '{self.user_id}')>"


# UserAnswer Table
class UserAnswer(db.Model):
    '''Storing users answers to questions for reference later
    '''
    __tablename__ = 'user_answers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True)
    question_id = db.Column(
        db.Integer,
        db.ForeignKey('questions.id', ondelete='CASCADE'),
        nullable=False,
        index=True)
    user_answer = db.Column(db.String(255))
    is_correct = db.Column(db.Boolean, nullable=False)
    answered_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', back_populates='answers')
    question = db.relationship('Question', back_populates='user_answer')

    def __repr__(self):
        """
        Returns a string representation of the UserAnswer instance.
        """
        return f"<UserAnswer('{self.user_answer}', '{self.is_correct}')>"
