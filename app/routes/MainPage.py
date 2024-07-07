from flask import Blueprint, render_template, current_app

main_page = Blueprint('main_page', __name__)

@main_page.route('/')
def index():
    return render_template('index.html', app_name=current_app.APP_NAME)
