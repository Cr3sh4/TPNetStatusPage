from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from app.config import DATABASE_NAME

# Create a blueprint
auth_bp = Blueprint('auth', __name__)

# User class
class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username


# User loader function
def load_user(user_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute('SELECT id, username FROM users WHERE id = ?', (user_id,))
    user_row = cursor.fetchone()
    connection.close()

    if user_row:
        return User(user_id=user_row[0], username=user_row[1])
    return None



# User registration validation
def validate_registration(username, password):
    if not username or not password:
        return render_template('auth/register.html', error='Username and password are required')
    if len(password) < 8:
        return render_template('auth/register.html', error='Password must be at least 8 characters long')
    if len(username) < 3:
        return render_template('auth/register.html', error='Username must be at least 3 characters long')
    if user_exists(username):
        return render_template('auth/register.html', error='Username already exists')

# Check if user exists
def user_exists(username):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user_row = cursor.fetchone()
    connection.close()

    if user_row is None:
        return False
    return True

def perform_registration(username, password):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    connection.commit()
    connection.close()

def perform_login(username, password):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
    user_row = cursor.fetchone()
    connection.close()

    if user_row:
        user = User(user_id=user_row[0], username=username)
        login_user(user)
        return render_template('index.html', app_name=current_app.APP_NAME)


# Routes

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
        user_row = cursor.fetchone()
        connection.close()

        if user_row:
            user = User(user_id=user_row[0], username=username)
            login_user(user)
            return redirect(url_for('auth.protected'))

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        validate_registration(username, password)
        perform_registration(username, password)
        perform_login(username, password)
        return render_template('auth/register.html', success='Registration successful')

@auth_bp.route('/protected')
@login_required
def protected():
    return render_template('index.html', app_name=current_app.APP_NAME)
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html', app_name=current_app.APP_NAME)

# Only for testing purposes
# @auth_bp.route('/status')
# def status():
#     if current_user.is_authenticated:
#         return 'Logged in as: ' + current_user.username + '<br>Id: ' + str(current_user.id) + '<br>User exists: ' + str(user_exists(current_user.username))
#     else:
#         return 'You are not logged in.'
