#!/usr/bin/env python3
""" App inititialization:
Blueprint registration
Extensions initialization
App configuration
"""
from flask import Flask
from .config import Config
from .extensions import db, migrate, bcrypt, login_manager
from .models.user import User


def create_app(config_class=Config):
    '''create_app:
    1. Initializes the flask app
    2. Sets up config
    3. Registers blueprints
    Returns:
        Configured app
    '''
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Login manager user loader
    @login_manager.user_loader
    def load_user(user_id):
        """User Loader
        """
        return User.query.get(int(user_id))

    # Register Blueprints

    return app
