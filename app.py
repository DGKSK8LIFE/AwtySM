from flask import Flask, render_template, request, session
import sqlite3

app = Flask(__name__)

# secret key for encryption and cookie security
app.secret_key = 'x3964njs2356xa'


restricted_chars = ('/', ';', '*', '=', '\'', '\"',
                    '#', '<', '>', '[', ']', '{', '}')


@app.route('/')
def login():
    return render_template('index.html')


@app.route('/create.html')
def show_create():
    return render_template('create.html')


@app.route('/events.html')
def events():
    return render_template('events.html')


@app.route('/memes.html')
def memes():
    return render_template('memes.html')


@app.route('/menu.html')
def menu():
    return render_template('menu.html')


@app.route('/news.html')
def news():
    return render_template('news.html')


@app.route('/sports.html')
def sports():
    return render_template('sports.html')


@app.route('/loggedin', methods=['GET', 'POST'])
def verify_login():
    username = request.form.get('username')
    password = request.form.get('password')
    session['name'] = username
    for i in restricted_chars:
        if i in username or i in password:
            return render_template('charerr.html')
    else:
        db = sqlite3.connect('accounts.sqlite')
        query = db.execute(
            f'SELECT * FROM accounts WHERE username=\'{username}\' AND password=\'{password}\';')
        account = query.fetchall()
        if account:
            db.close()
            return render_template('menu.html', username=session.get('name'))
        db.close()
        return render_template('index.html')


@app.route('/created', methods=['POST'])
def create_account():
    username = request.form.get('username')
    password = request.form.get('password')
    db = sqlite3.connect('accounts.sqlite')
    for i in restricted_chars:
        if i in username or i in password:
            return render_template('charerr.html')
    else:
        q = db.execute(
            f'SELECT * FROM accounts WHERE username=\'{username}\';')
        if not q.fetchone():
            db.execute(
                f'INSERT INTO accounts VALUES (\'{username}\', \'{password}\');')
            db.commit()
            db.close()
            return render_template('index.html')
        else:
            return render_template('taken.html')
