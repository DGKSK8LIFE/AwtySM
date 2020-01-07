from flask import Flask, render_template, request, session, make_response
import sqlite3

app = Flask(__name__)

app.secret_key = "x3964njs2356xa28169asdfmvm"

restricted_chars = ("/", ";", "*", "=", "'", '"',
                    "#", "<", ">", "[", "]", "{", "}")


@app.route("/")
def login():
    return render_template("index.html")


@app.route("/create.html")
def show_create():
    return render_template("create.html")


@app.route("/events.html")
def events():
    if request.cookies.get('loggedin?'):
        return render_template("events.html")
    else:
        return render_template("loginerr.html")


@app.route("/memes.html")
def memes():
    if request.cookies.get('loggedin?'):
        return render_template("memes.html")
    else:
        return render_template("loginerr.html")


@app.route("/news.html")
def news():
    if request.cookies.get('loggedin?'):
        return render_template("news.html")
    else:
        return render_template("loginerr.html")


@app.route("/sports.html")
def sports():
    if request.cookies.get('loggedin?'):
        return render_template("sports.html")
    else:
        return render_template("loginerr.html")


@app.route("/about.html")
def about():
    if request.cookies.get('loggedin?'):
        return render_template("about.html")
    else:
        return render_template("loginerr.html")


""" gets username and password -> checks if they contain restricted characters ->
    validate them in the database -> send to menu """


@app.route("/loggedin", methods=["POST", "GET"])
def verify_login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username and password:
        for i in restricted_chars:
            if i in username or i in password:
                return render_template("charerr.html")
        else:
            try:
                db = sqlite3.connect("accounts.sqlite")
                query = db.execute(
                    f"SELECT * FROM accounts WHERE username='{username}' AND password='{password}';"
                )
                account = query.fetchall()
                if account:
                    session["name"] = username

                    resp = make_response(render_template(
                        "menu.html", username=session.get("name")))
                    resp.set_cookie('loggedin?', True)

                    return resp
                resp.set_cookie('loggedin?', False)
                return render_template("index.html")
            finally:
                db.close()
    else:
        return render_template("loginerr.html")


""" gets username & password -> checks to see if they contain illegal characters 
    -> writes the credentials to the accounts.sqlite database -> redirects to login.html """


@app.route("/created", methods=["POST"])
def create_account():
    username = request.form.get("username")
    password = request.form.get("password")
    for i in restricted_chars:
        if i in username or i in password:
            return render_template("charerr.html")
    else:
        try:
            db = sqlite3.connect("accounts.sqlite")
            q = db.execute(
                f"SELECT * FROM accounts WHERE username='{username}';")
            if not q.fetchone():
                db.execute(
                    f"INSERT INTO accounts VALUES ('{username}', '{password}');")
                db.commit()
                return render_template("index.html")
            else:
                return render_template("taken.html")
        finally:
            db.close()
