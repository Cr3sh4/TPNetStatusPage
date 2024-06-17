from flask import Flask
from .config import SECRET_KEY


def create_app():
    app = Flask(__name__)
    app.SECRET_KEY = SECRET_KEY
    # Register blueprints

    from app.routes.MainPage import main_page  # Main Page
    app.register_blueprint(main_page)

    return app
