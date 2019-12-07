from flask import Flask, render_template
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
    if not username or not password:
        return render_template('failpage.html')
    else:
        db = sqlite3.connect('accounts.sqlite')
        query = db.execute(
            f'SELECT * FROM ACCOUNT WHERE username=\'{username}\' AND password=\'{password}\';')
        account = query.fetchall()
        if account:
            db.close()
            # allow users to access dashboard here
        # close db and display a fail message
        db.close()
        return render_template('index.html')
