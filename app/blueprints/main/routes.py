#!/usr/bin/env python3
''' routes:
Module for all the routes under main blueprint
'''
from flask import render_template
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