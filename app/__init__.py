#!/usr/bin/env python3
""" App inititialization:
Blueprint registration
Extensions initialization
App configuration
"""
import firebase_admin
from firebase_admin import credentials
from flask import Flask
from .config import Config
from .extensions import db, migrate, bcrypt, login_manager
from .models.user import User, Score
from .models.resources import Category, Question, CategoryQuestion, Comment
from .blueprints.main import main_bp
from .blueprints.admin import admin_bp
from .blueprints.auth import auth_bp


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

    # Firebase Admin
    cred = credentials.Certificate("./app/firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)

    # Login manager user loader
    @login_manager.user_loader
    def load_user(user_id):
        """User Loader
        """
        return User.query.get(int(user_id.split(":")[1]))

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
