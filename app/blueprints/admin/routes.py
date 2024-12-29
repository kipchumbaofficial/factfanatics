#!/usr/bin/env python3
'''routes:
Contains all the views of the admin blueprint
'''
from flask import redirect, url_for, render_template
from flask_login import login_required
from app.models.user import User
from app.utils.login_utils import admin_required
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
    return render_template('admin/dashboard.html')
