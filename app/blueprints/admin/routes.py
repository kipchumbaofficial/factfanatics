#!/usr/bin/env python3
'''routes:
Contains all the views of the admin blueprint
'''
from . import admin_bp


@admin_bp.route('/')
def dashboard():
    '''dashboard
    Admin dashboard for managing questions and comments
    '''
    return 'Hello Admin'
