from flask import Flask, render_template, request
from flask import Flask, request, redirect, url_for, render_template, session
import sqlite3
import threading

app = Flask(__name__)
app.secret_key = 'my_secret_key'

CountGrp = 0
CountFrnd = 0


def get_db():
    if not hasattr(thread_local, 'connection'):
        thread_local.connection = sqlite3.connect('mydatabase.db')
    return thread_local.connection

thread_local = threading.local()


@app.route('/')
def index():
    return render_template('externalhome.html')

username = ""

@app.route('/login', methods=['POST'])
def login():
    global username
    username = request.form['username']
    password = request.form['password']
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            USER_NAME TEXT,
                            PAY INTEGER,
                            RECEIVE INTEGER
                        )''')
        cursor.execute("SELECT * FROM users WHERE user_name=?", (username,))
        user = cursor.fetchone()
        if user is None:
            cursor.execute(
                'INSERT INTO users (user_name) VALUES (?)', (username,))
            connection.commit()

    session['username'] = username
    return redirect(url_for('dashboard'))


@app.route('/login.html')
def log():
    return render_template('login.html')


@app.route('/dashbrd.html')
def dashboard():
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM users WHERE user_name=?", (username,))
        f = cursor.fetchone()
        if f is None:
            return redirect(url_for("log"))
        uId = f[0]
        # print(uId)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS GROUPS (Group_ID INTEGER PRIMARY KEY, Group_Name TEXT NOT NULL, USER_ID INTEGER);")
        cursor.execute(f'SELECT * FROM Groups WHERE USER_ID='+str(uId))
        groups = cursor.fetchall()
        group_friends = []
        for group in groups:
            cursor.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{"GROUP_"+str(group[0])}'""")
            h = cursor.fetchall()
            # print(h)
            if h == []:
                group_friends.append([])
            else:
                frnds = []
                cursor.execute("SELECT USER_NAME FROM GROUP_"+str(group[0]))
                k = cursor.fetchall()
                for friend in k:
                    frnds.append(friend[0])
                group_friends.append(frnds)
        friend_names = []
        cursor.execute("CREATE TABLE IF NOT EXISTS Friendship (ID INTEGER PRIMARY KEY AUTOINCREMENT,USER_ID INTEGER, FRIEND_ID INTEGER, PAY INTEGER, RECEIVE INTEGER);")
        cursor.execute("SELECT * FROM Friendship WHERE USER_ID="+str(uId))
        friends = cursor.fetchall()
        for friend in friends:
            cursor.execute("SELECT USER_NAME FROM USERS WHERE ID="+str(friend[2]))
            friend_names.append(cursor.fetchone()[0])
        cursor.execute("SELECT * FROM FRIENDSHIP WHERE FRIEND_ID="+str(uId))
        friends = cursor.fetchall()
        for friend in friends:
            cursor.execute("SELECT USER_NAME FROM USERS WHERE ID="+str(friend[1]))
            friend_names.append(cursor.fetchone()[0])
        # print(friend_names)
    return render_template('dashbrd.html', groups=groups, friends=friend_names, group_friends=group_friends)

@app.route('/add_group', methods=['POST'])
def add_group():
    group = request.form['group']
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM Users WHERE USER_NAME='"+username+"'")
        user_id = cursor.fetchone()[0]
        cursor.execute("SELECT GROUP_NAME FROM Groups WHERE USER_ID="+str(user_id))
        all = cursor.fetchall()
        print(all)
        if group not in [el[0] for el in all]:
            cursor.execute("SELECT MAX(GROUP_ID) FROM GROUPS")
            count = 1
            f = cursor.fetchone()
            if f[0] is not None:
                count = f[0]+1
                print(count)
            cursor.execute('INSERT INTO Groups(GROUP_ID, GROUP_NAME, USER_ID) VALUES (?, ?, ?)', (count, group, user_id))
            connection.commit()
    return redirect('/dashbrd.html')

@app.route("/add_group_friend", methods=['POST'])
def addtogroup():
    name = request.form['name']
    gid = request.form['gid']
    connection = sqlite3.connect("mydatabase.db")
    cur = connection.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS GROUP_{gid}(ID INTEGER PRIMARY KEY AUTOINCREMENT, USER_NAME TEXT)")
    cur.execute(f"INSERT INTO GROUP_{gid}(USER_NAME) VALUES (?)", (name,))
    cur.execute("SELECT * FROM GROUP_"+gid)
    print(cur.fetchall())
    print(name)
    connection.commit()
    return redirect(url_for("dashboard"))

@app.route('/add_friend', methods=['POST'])
def add_friend():
    friend = request.form['friend']
    # print(friend)
    with get_db() as connection:
        cursor = connection.cursor()
        print(username)
        s = cursor.execute("SELECT * FROM Users where USER_NAME='"+username+"'").fetchone()
        user_id = s[0]
        cursor.execute("SELECT ID FROM USERS WHERE USER_NAME='"+friend+"'")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO USERS (USER_NAME, PAY, RECEIVE) VALUES (?,?,?)", (friend, 0, 0))
        cursor.execute("SELECT ID FROM USERS WHERE USER_NAME='"+friend+"'")
        friend_id = cursor.fetchone()[0]
        print(friend_id)
        cursor.execute("INSERT INTO FRIENDSHIP (USER_ID, FRIEND_ID, PAY, RECEIVE) VALUES (?,?,?,?)", (user_id, friend_id, 0, 0))
        connection.commit()
    return redirect('/dashbrd.html')

@app.route('/externalhome.html')
def externalhome():
    return render_template('externalhome.html')


@app.route('/add_expense.html')
def add_expense():
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM users WHERE user_name=?", (username,))
        f = cursor.fetchone()
        if f is None:
            return redirect(url_for("log"))
        uId = f[0]
        # print(uId)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS GROUPS (Group_ID INTEGER PRIMARY KEY, Group_Name TEXT NOT NULL, USER_ID INTEGER);")
        cursor.execute(f'SELECT * FROM Groups WHERE USER_ID='+str(uId))
        groups = cursor.fetchall()
        group_friends = []
        for group in groups:
            cursor.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{"GROUP_"+str(group[0])}'""")
            h = cursor.fetchall()
            # print(h)
            if h == []:
                group_friends.append([])
            else:
                frnds = []
                cursor.execute("SELECT USER_NAME FROM GROUP_"+str(group[0]))
                k = cursor.fetchall()
                for friend in k:
                    frnds.append(friend[0])
                group_friends.append(frnds)
        friend_names = []
        cursor.execute("CREATE TABLE IF NOT EXISTS Friendship (ID INTEGER PRIMARY KEY AUTOINCREMENT,USER_ID INTEGER, FRIEND_ID INTEGER, PAY INTEGER, RECEIVE INTEGER);")
        cursor.execute("SELECT * FROM Friendship WHERE USER_ID="+str(uId))
        friends = cursor.fetchall()
        for friend in friends:
            cursor.execute("SELECT USER_NAME FROM USERS WHERE ID="+str(friend[2]))
            friend_names.append(cursor.fetchone()[0])
        cursor.execute("SELECT * FROM FRIENDSHIP WHERE FRIEND_ID="+str(uId))
        friends = cursor.fetchall()
        for friend in friends:
            cursor.execute("SELECT USER_NAME FROM USERS WHERE ID="+str(friend[1]))
            friend_names.append(cursor.fetchone()[0])
        # print(friend_names)
    return render_template('add_expense.html', groups=groups, friends=friend_names, group_friends=group_friends)


if __name__ == '__main__':
    app.run(debug=True)
