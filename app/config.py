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
    @property
    def secret_key(self):
        '''secret_key
        '''
        return os.getenv('SECRET_KEY')

    @property
    def sqlalchemy_database_uri(self):
        '''Database URI
        '''
        return os.getenv('SQLALCHEMY_DATABASE_URI')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
