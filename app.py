from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("index.html")


@app.route('/loggedin', methods=['POST'])
def verify_login():
    username = request.form.get('username')
    password = request.form.get('password')
    db = sqlite3.connect('accounts.sqlite')
    query = db.execute(
        f'SELECT * FROM accounts WHERE username=\'{username}\' AND password=\'{password}\';')
    account = query.fetchall()
    if account:
        db.close()
        return "success"
    # allow users to access dashboard here
    # close db and reload homepage
    db.close()
    return render_template('index.html')
