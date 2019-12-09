from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

restricted_chars = ('/', ';', '*', '=', '\'', '\"',
                    '#', '<', '>', '[', ']', '{', '}')


@app.route('/')
def login():
    return render_template('index.html')


@app.route('/create.html')
def show_create():
    return render_template('create.html')


@app.route('/chat.html')
def chat():
    return render_template('chat.html')


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


@app.route('/loggedin', methods=['POST'])
def verify_login():
    username = request.form.get('username')
    password = request.form.get('password')
    for i in restricted_chars:
        if i in username:
            return 'you inputted illegal characters! GTFO'
    else:
        db = sqlite3.connect('accounts.sqlite')
        query = db.execute(
            f'SELECT * FROM accounts WHERE username=\'{username}\' AND password=\'{password}\';')
        account = query.fetchall()
        if account:
            db.close()
            return render_template('menu.html')
        # allow users to access dashboard here
        # close db and reload homepage
        db.close()
        return render_template('index.html')


@app.route('/created', methods=['POST'])
def create_account():
    username = request.form.get('username')
    password = request.form.get('password')
    db = sqlite3.connect('accounts.sqlite')
    q = db.execute(
        f'SELECT * FROM accounts WHERE username=\'{username}\';')
    if not q.fetchone():
        db.execute(
            f'INSERT INTO accounts VALUES (\'{username}\', \'{password}\');')
        db.commit()
        db.close()
        """ going to allow entry here and give the user some kind of affirmation that their
        accounts was created """
        return render_template('index.html')
    else:
        return 'That username is taken! Please choose a different one'
