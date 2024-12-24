#!/usr/bin/env python3
""" Config module:
        Contains configuration class
"""
import os
from dotenv import load_dotenv

# Load Variables from .env file
load_dotenv()


class Config:
    """Config class for application configurations.
    """
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
