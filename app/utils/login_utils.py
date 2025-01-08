#!usr/bin/env python3
""" Login utilities
"""
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """ Check if the user is admin
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """ Checks if the current user is an admin
        """
        if not current_user.is_authenticated:  # Check if the user is logged in
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('main.login'))

        if not current_user.is_admin:  # Check if the logged-in user is an admin
            flash('You must be an admin to access this page.', 'error')
            return redirect(url_for('main.result'))

        return f(*args, **kwargs)
    return decorated_function
