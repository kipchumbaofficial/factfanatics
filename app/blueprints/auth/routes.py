#!/usr/bin/env python3
'''routes:
All the routes in the auth blueprint
'''
from flask import request, jsonify, redirect, url_for
from firebase_admin import auth as firebase_auth
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.user import User
from . import auth_bp


# Login Route
@auth_bp.route('/login', methods=['POST'])
def login():
    '''Handles Google Sign-In using Firebase
    '''
    try:
        # Getthe ID token from the request
        id_token = request.json.get('id_token')

        # Verify the ID token using firebase Admin SDK
        decoded_token = firebase_auth.verify_id_token(id_token)
        email = decoded_token.get('email')
        name = decoded_token.get('name')

        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                username=name,
                email=email
            )
            db.session.add(user)
            db.session.commit()

        # log the user in using Flask-Login
        login_user(user, remember=True)

        # Return JSON success response
        return jsonify({
            'status': 'success',
            'message': 'User logged in successfully'
        })
    except (ValueError, KeyError, SQLAlchemyError):
        return jsonify({
            'status': 'error',
            'message': 'Login failed.'
        }), 401


@auth_bp.route('/initialize', methods=['POST'])
def initialize_admin():
    """ Create a new admin
    """
    # Register the first admin
    try:
        # Get the ID token from the request
        id_token = request.json.get('id_token')

        # Verify the ID token using Firebase Admin SDk
        decoded_token = firebase_auth.verify_id_token(id_token)
        user_email = decoded_token.get('email')
        user_name = decoded_token.get('name')

        # Check if the user exists in the database
        user = User.query.filter_by(email=user_email).first()
        if user:
            user.is_admin = True
        if not user:
            # If the user doesn't exist create a new user
            user = User(
                username=user_name,
                email=user_email,
                is_admin=True
            )
            db.session.add(user)
        db.session.commit()

        # Log the user in using Flask-Login
        login_user(user, remember=True)

        # Return JSON success response
        return jsonify({
            'status': 'success',
            'message': 'User logged in successfully'
        })
    except (ValueError, KeyError, SQLAlchemyError):
        return jsonify({
            'status': 'error',
            'message': 'Login failed.'
        }), 401


@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    """Logs out users
    """
    logout_user()
    return redirect(url_for('main.home'))


@auth_bp.route('/check-login-status', methods=['GET'])
def check_login_status():
    """ Return the login status of the user
    """
    return jsonify({
        'logged_in': current_user.is_authenticated
    })
