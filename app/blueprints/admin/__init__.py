#!/usr/bin/env python3
''' Initializes the admin blueprint
'''
from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

from . import routes