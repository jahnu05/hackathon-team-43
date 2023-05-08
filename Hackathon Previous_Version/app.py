from flask import Flask, request, redirect, url_for, render_template, session
import sqlite3
import threading

app = Flask(__name__)
app.secret_key = 'my_secret_key'

CountGrp = 0
CountFrnd=0
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
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    global username
    username = request.form['username']
    password = request.form['password']

    # Check if the user_name already exists in the users table
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (ID INTEGER PRIMARY KEY AUTOINCREMENT, User_Name TEXT);")
        connection.commit()
        cursor.execute("SELECT * FROM users WHERE user_name=?", (username,))
        user = cursor.fetchone()
        if user is None:
            # Insert the user_name into the users table
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_name TEXT
                        )''')
            cursor.execute('INSERT INTO users (user_name) VALUES (?)', (username,))
            connection.commit()

    # Store the username in the session object
    session['username'] = username

    return redirect(url_for('dashboard'))


@app.route('/dashbrd.html')
def dashboard():
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM users WHERE user_name=?", (username,))
        uId = cursor.fetchone()[0]
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Groups (Group_ID INTEGER PRIMARY KEY, Group_Name TEXT NOT NULL, User_ID INTEGER);")
        cursor.execute('SELECT * FROM Groups;')
        h = cursor.fetchall()
        global CountGrp
        CountGrp = len(h) + 1
        groups = []
        for row in h:
            if row[2]==uId:
                groups.append(row[1])
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Friends (Friend_ID INTEGER PRIMARY KEY, Friend_Name TEXT NOT NULL, User_ID INTEGER);")
        cursor.execute("SELECT * FROM Friends;")
        g = cursor.fetchall()
        global CountFrnd
        CountFrnd = len(g) + 1
        friends=[]
        for row in g:
            if row[2]==uId:
                friends.append(row[1])
    return render_template('dashbrd.html', groups=groups, friends=friends)


@app.route('/add_group', methods=['POST'])
def add_group():
    global CountGrp
    group = request.form['group']
    with get_db() as connection:
        cursor = connection.cursor()
        s=cursor.execute("SELECT * FROM Users;").fetchall()
        users=[row for row in s]
        uID=0
        for i in users:
            if i[1]==username:
                uID=i[0]  
        h=cursor.execute("SELECT * FROM Groups").fetchall()
        groups=[row[1] for row in h]
        flag=1
        for i in groups:
            if i==group:
                flag=0
                break
        if flag==1:
            cursor.execute('INSERT INTO Groups VALUES (?, ?, ?)', (CountGrp, group, uID))
            connection.commit()
            CountGrp += 1
    return redirect('/dashbrd.html')


@app.route('/add_friend', methods=['POST'])
def add_friend():
    global CountFrnd
    friend = request.form['friend']
    with get_db() as connection:
        cursor = connection.cursor()
        s=cursor.execute("SELECT * FROM Users;").fetchall()
        users=[row for row in s]
        uID=0
        for i in users:
            if i[1]==username:
                uID=i[0]   
        h=cursor.execute("SELECT * FROM Friends;").fetchall()
        friends=[row[1] for row in h]
        flag=1
        for i in friends:
            if i==friend:
                flag=0
                break
        if flag==1:
            cursor.execute('INSERT INTO Friends VALUES (?, ?, ?)', (CountFrnd, friend, uID))
            connection.commit()
            CountFrnd += 1
    return redirect('/dashbrd.html')

@app.route('/externalhome.html')
def externalhome():
    return render_template('externalhome.html')

@app.route('/add_expense.html')
def add_expense():
    return render_template('add_expense.html')

if __name__ == '__main__':
    app.run(debug=True)
