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

    scores = db.relationship('Score', backref='user')
    comments = db.relationship('UserComment', back_populates='user')

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
    user_id = db.Column(db.Integer, db.ForegignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.Datetime, default=datetime.now)

    def __repr__(self):
        """
        Returns a string representation of the Score instance.
        """
        return f"<Score('{self.value}')>"


class UserComment(db.Model):
    '''UserComment
    Associative table for users and comments
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))

    user = db.relationship('User', back_populates='comments')
    comment = db.relationship('Comment', back_populates='user_comments')

    def __repr__(self):
        """
        Returns a string representation of the Score instance.
        """
        return f"<Score('{self.comment}')>"
