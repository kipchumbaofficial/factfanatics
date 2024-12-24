#!/usr/bin/env python3
''' Initialize the main blue print
'''
from flask import Blueprint

main_bp = Blueprint('main', __name__)

from . import routes