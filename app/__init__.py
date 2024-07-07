from flask import Flask
from flask_login import LoginManager
from .config import SECRET_KEY, APP_NAME
from app.dbManager import init_db


def create_app():
    # Init database
    init_db()

    # Create app
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.APP_NAME = APP_NAME

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # User loader function
    from app.routes.Authorization.Auth import load_user
    login_manager.user_loader(load_user)

    # Register blueprints
    from app.routes.MainPage import main_page  # Main Page
    from app.routes.Authorization.Auth import auth_bp  # Auth Page

    app.register_blueprint(main_page)
    app.register_blueprint(auth_bp)

    return app
