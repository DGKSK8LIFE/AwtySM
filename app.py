from flask import Flask, render_template, request, session, make_response
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)

app.secret_key = "x3964njs2356xa28169asdfmvm"

restricted_chars = ("/", ";", "*", "=", "'", '"',
                    "#", "<", ">", "[", "]", "{", "}")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('custom_err.html', error='404 Not Found'), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('custom_err.html', error='Method Not Allowed'), 405


@app.route("/")
def login():
    return render_template("index.html")


@app.route("/create.html")
def show_create():
    return render_template("create.html")


@app.route("/events.html")
def events():
    if request.cookies.get('loggedin?') == "True":
        return render_template("events.html")
    else:
        return render_template("custom_err.html", error='You must be logged in to view exclusive content.')


@app.route("/memes.html")
def memes():
    if request.cookies.get('loggedin?') == "True":
        return render_template("memes.html")
    else:
        return render_template("custom_err.html", error='You must be logged in to view exclusive content.')


@app.route("/news.html")
def news():
    if request.cookies.get('loggedin?') == "True":
        return render_template("news.html")
    else:
        return render_template("custom_err.html", error='You must be logged in to view exclusive content.')


@app.route("/sports.html")
def sports():
    if request.cookies.get('loggedin?') == "True":
        return render_template("sports.html")
    else:
        return render_template("custom_err.html", error='You must be logged in to view exclusive content.')


@app.route("/about.html")
def about():
    if request.cookies.get('loggedin?') == "True":
        return render_template("about.html")
    else:
        return render_template("custom_err.html", error='You must be logged in to view exclusive content.')


@app.route('/session.html')
def sessions():
    if request.cookies.get('loggedin?') == "True":
        return render_template('session.html')
    else:
        return render_template("custom_err.html", error='You must be logged in to view exclusive content.')


def message_received(methods=['GET', 'POST']):
    print('message was received!')


@socketio.on('my event')
def handle_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=message_received)


""" gets username and password -> checks if they contain restricted characters ->
    validate them in the database -> send to menu """


@app.route("/loggedin", methods=["POST", "GET"])
def verify_login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username and password:
        for i in restricted_chars:
            if i in username or i in password:
                return render_template("custom_err.html", error='Account credentials cannot contain illegal characters!')
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
                    resp.set_cookie('loggedin?', "True")

                    return resp
                resp = make_response(render_template('index.html'))
                resp.set_cookie('loggedin?', "False")
                return resp
            finally:
                db.close()
    else:
        return render_template("custom_err.html", error='You must be logged in to view exclusive content.')


""" gets username & password -> checks to see if they contain illegal characters 
    -> writes the credentials to the accounts.sqlite database -> redirects to login.html """


@app.route("/created", methods=["POST"])
def create_account():
    username = request.form.get("username")
    password = request.form.get("password")
    for i in restricted_chars:
        if i in username or i in password:
            return render_template("custom_err.html", error='Accounts credentials cannot contain illegal characters.')
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

@app.route('/creators')
def creators():
    return render_template("creators.html", name1 = "AVCADO", name2 = "DGKSK8LIFE")

if __name__ == '__main__':
    socketio.run(app)
