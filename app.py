from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("index.html")

@app.route("/loggedin")
def auth():
    