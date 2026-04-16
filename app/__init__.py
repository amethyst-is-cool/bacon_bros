import sqlite3
import random
from flask import Flask, render_template
from flask import session, request, redirect


# Flask
app = Flask(__name__)
app.secret_key = 'wegjedfoigshseiudf'

# SQLite

DB_FILE = "data.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    #conn.execute("PRAGMA foreign_keys = ON;")
    return conn

db = get_db()

c = db.cursor()


c.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
    username TEXT UNIQUE,
    password TEXT,
    pFoods TEXT,
    pExercises TEXT)
    """
)


db.commit()
db.close()


@app.route('/', methods=["GET", "POST"])
def homepage():
    if "username" not in session:
        return redirect("/login")
    return render_template("home.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usernames = [row[0] for row in fetch("users", "TRUE", "username")]
        if not request.form["username"] in usernames:
            return render_template("login.html", error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>")
        elif (request.form["password"] != fetch("users", "username = ?", "password", (request.form["username"],))[0][0]):
            return render_template("login.html", error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>")
        else:
            session["username"] = request.form["username"]

    if "username" in session:
        return redirect("/")

    return render_template("login.html")






@app.route('/register', methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect("/")

    if request.method == "POST" and request.form:
        usernames = [row[0] for row in fetch("users", "TRUE", "username")]
        if request.form["username"] in usernames:
            return render_template("register.html", error="Username already taken, please try again! <br><br>")
       # elif request.form["password"] != request.form["confirm"]:
        #    return render_template("register.html", error="Passwords don't match! <br><br>")
        else:
            db = sqlite3.connect(DB_FILE)
            c = db.cursor()
            c.execute(
                "INSERT INTO users VALUES (?, ?, ?, ?)",
                (
                    request.form["username"],
                    request.form["password"],
                    "",
                    ""
                )
            )
            db.commit()
            db.close()
            session["username"] = fetch("users", "username = ?", "username", (request.form["username"],))[0][0]
            return redirect("/")

    return render_template("register.html")




@app.route('/profile', methods=["GET", "POST"])
def profile():
    if "username" not in session:
        return redirect("/login")
    user = session["username"]
    food = fetch("users", "username = ?", "pFoods", (session["username"],))[0][0]
    exer = fetch("users", "username = ?", "pExercises", (session["username"],))[0][0]
    d1 = True
    d2 = True

    if request.method == "POST":
        if "foodEdit" in request.form:
            return render_template("profile.html", user = user, d1 = False, d2 = d2, food = food, exercises = exer)
        if "foodsSub" in request.form:
            update_userinfo(session["username"], "pFoods", food + request.form["idk"])
            food = fetch("users", "username = ?", "pFoods", (session["username"],))[0][0]
            return render_template("profile.html", user = user, d1 = True, d2 = d2, food = food, exercises = exer)

        if "exerEdit" in request.form:
            return render_template("profile.html", user = user, d1 = d1, d2 = False, food = food, exercises = exer)
        if "exerSub" in request.form:
            update_userinfo(session["username"], "pExercises", exer + request.form["idk2"])
            exer = fetch("users", "username = ?", "pExercises", (session["username"],))[0][0]
            return render_template("profile.html", user = user, d1 = d1, d2 = True, food = food, exercises = exer)

    return render_template("profile.html", user = user, d1 = True, d2 = True, food = food, exercises = exer)

@app.route('/explore', methods=["GET", "POST"])
def explore():
    if "username" not in session:
        return redirect("/login")

    return render_template("chart.html", labels = ["test1", "test2", "test3", "test4", "test5"], values = [5, 10, 15, 25, 30])

@app.route('/personalize', methods=["GET", "POST"])
def personalize():
    if "username" not in session:
        return redirect("/login")

    user = session["username"]
    food = fetch("users", "username = ?", "pFoods", (session["username"],))[0][0]
    exer = fetch("users", "username = ?", "pExercises", (session["username"],))[0][0]

    return render_template("exercise.html", user=user, food=food, exercise=exer)





@app.route("/explore", methods=["GET", "POST"])
def chart():
    if "username" not in session:
        return redirect("/login")

    return render_template("chart.html", labels = ["test1", "test2", "test3", "test4", "test5"], values = [5, 10, 15, 25, 30])








@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/login")


def fetch(table, criteria, data, params=()):
    db = get_db()
    c = db.cursor()
    query = f"SELECT {data} FROM {table} WHERE {criteria}"
    c.execute(query, params)
    data = c.fetchall()
    db.close()
    return data

def update_userinfo(user, kind, info):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(f"UPDATE users SET {kind} = ? WHERE username=?", (info, user))
    db.commit()
    db.close()


# Flask
if __name__=='__main__':
    app.debug = False
    app.run()
