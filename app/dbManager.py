import sqlite3
from app.config import DATABASE_NAME


def init_db():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS "users" (
        "id"	INTEGER,
        "username"	TEXT,
        "password"	TEXT,
        "email"	TEXT,
        "rank"	INTEGER DEFAULT 0,
        PRIMARY KEY("id" AUTOINCREMENT)
    )''')
    # Add a default user
    insert_default_user = "INSERT INTO users (username, password, email, rank) SELECT ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = ?)"
    cursor.execute(insert_default_user, ('admin', 'letmein', 'admin@example.com', 100, 'admin'))

    connection.commit()
    connection.close()


def query_fetch_one(query, params):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(query, (params))
    user_row = cursor.fetchone()
    connection.close()

    return user_row

    # connection = sqlite3.connect('database.db')
    # cursor = connection.cursor()
    # cursor.execute(query)
    # result = cursor.fetchall()
    # connection.close()
    # return result

def get_email(email):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT email FROM users WHERE email=?", (email))
    result = cursor.fetchall()
    connection.close()
    return result

def create_user(username, password, email):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
    connection.commit()
    connection.close()
