from flask import Flask, request, redirect, url_for, render_template, session
import sqlite3
import threading

app = Flask(__name__)
app.secret_key = 'my_secret_key'

friends = []
count = 0

# Create a new connection for each thread
def get_db():
    if not hasattr(thread_local, 'connection'):
        thread_local.connection = sqlite3.connect('mydatabase.db')
    return thread_local.connection


# Initialize thread-local storage
thread_local = threading.local()

# Define the routes
@app.route('/')
def index():
    return render_template('externalhome.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the user_name already exists in the users table
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name=?", (username,))
        user = cursor.fetchone()
        if user is None:
            # Insert the user_name into the users table
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_name TEXT
                        )''')
            cursor.execute('INSERT INTO users (user_name) VALUES (?)', (username,))
            connection.commit()

    # Store the username in the session object
    session['username'] = username

    return redirect(url_for('dashboard'))

@app.route('/login.html')
def log():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)