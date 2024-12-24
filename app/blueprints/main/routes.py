#!/usr/bin/env python3
''' routes:
Module for all the routes under main blueprint
'''
from flask import jsonify
from . import main_bp


@main_bp.route('/')
def home():
    '''Home route
    '''
    return jsonify({
        'Tagline': 'Factfanatics smoking facts yall be smoking make belief'
        })