import sqlite3
import random
from flask import Flask, render_template
from flask import session, request, redirect
import data

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


c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT UNIQUE,
    password TEXT,
    age INT,
    weight INT,
    height INT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS user_foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    name TEXT,
    calories INTEGER,
    fat REAL,
    sugar REAL,
    protein REAL,
    fiber REAL,
    cholesterol REAL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS user_exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    age INT,
    gender TEXT,
    weight REAL,
    height REAL,
    session_duration REAL,
    calories_burned REAL,
    workout_type TEXT,
    BMI REAL,
    name TEXT,
    sets INT,
    reps INT,
    benefit TEXT,
    burns_calories REAL,
    target_muscle_group TEXT,
    workout TEXT
)
""")

#temporary food preferences for user with username a
c.execute("""
INSERT INTO user_foods
(username, name, calories, fat, sugar, protein, fiber, cholesterol)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", ('a', 'Apple', 95, 0.3, 19, 0.5, 4.4, 0))

c.execute("""
INSERT INTO user_exercises
(username, age, gender, weight, height, session_duration, calories_burned, workout_type, BMI, name, sets, reps, benefit, burns_calories, target_muscle_group, workout )
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", ('a', 0, "male", 0.3, 1.9, 0.5, 4.4, "abs", 9.0, "crunch", 9, 2, "good", 20.3, "gut", "lala"))

db.commit()
db.close()


@app.route('/', methods=["GET", "POST"])
def homepage():
    if "username" not in session:
        return redirect("/login")
    return render_template("home.html", food_search = None)


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
                "INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                (
                    request.form["username"],
                    request.form["password"],
                    0,
                    0,
                    0
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
    
    db = get_db()
    c = db.cursor()

    user = session["username"]

    food = fetch("users", "username = ?", "username", (session["username"],))[0][0]
    exer = fetch("users", "username = ?", "username", (session["username"],))[0][0]

    age = fetch("users", "username = ?", "age", (session["username"],))[0][0]
    height = fetch("users", "username = ?", "height", (session["username"],))[0][0]
    weight = fetch("users", "username = ?", "weight", (session["username"],))[0][0]

    foods = getFoodsList(True, "name")

    foodsL = []
    for i in range(1, len(foods)):
        foodsL += [foods[i][0]]

    if height != 0 and age != 0 and weight != 0:
        haveInfo = True
    else:
        haveInfo = False

    d = True
    d2 = True

    if request.method == "POST":
        
        if "exerEdit" in request.form:
            return render_template("profile.html", user = user, d= d, d2 = False, food = food, exercises = exer, age = age, height = height, weight = weight, foods = foodsL)
        if "exerSub" in request.form:
            update_userinfo(session["username"], "pExercises", exer + request.form["idk2"])
            exer = fetch("users", "username = ?", "pExercises", (session["username"],))[0][0]
            return render_template("profile.html", user = user, d=d, d2 = True, food = food, exercises = exer, age = age, height = height, weight = weight, foods = foodsL)

        if "infoEdit" in request.form:
            return render_template("profile.html", user = user, d= False, d2 = d2, food = food, exercises = exer, age = age, height = height, weight = weight, foods = foodsL)
       
        if "newInfo" in request.form:
            g = True
            



    return render_template("profile.html", user = user, d= True, d2 = True, food = food, exercises = exer, age = age, height = height, weight = weight, foods = foodsL)


@app.route('/explore', methods=["GET", "POST"])
def explore():
    if "username" not in session:
        return redirect("/login")

    return render_template("chart.html", labels = ["test1", "test2", "test3", "test4", "test5"], values = [5, 10, 15, 25, 30])

#personalize is responsible for displaying info about your food and exerc preferences
@app.route('/personalize', methods=["GET", "POST"])
def personalize():
    if "username" not in session:
        return redirect("/login")

    #have to tap into db again to get the user preferences tables to be able to rmv some
    db = get_db()
    c = db.cursor()

    user = session["username"]

    #pulls list of food
    food = c.execute("""
        SELECT name, calories, fat, sugar, protein, fiber, cholesterol
        FROM user_foods
        WHERE username = ?
    """, (user,)).fetchall()

    #temporary pull of exers
    exer = c.execute("""
        SELECT username, age, gender, weight, height, session_duration, calories_burned, workout_type, BMI, name, sets, reps, benefit, burns_calories, target_muscle_group, workout
        FROM user_exercises
        WHERE username = ?
    """, (user,)).fetchall()

    #if the button is pressed to remove that food from list
    if request.method == 'POST':
        if request.form.get("action") == "remove_food":
            food_name = request.form.get("food_name")

            c.execute("""
                DELETE FROM user_foods
                WHERE username = ? AND name = ?
            """, (user, food_name))

            db.commit()
            return redirect("/personalize")

    if request.method == 'POST':
        if request.form.get("action") == "remove_exercise":
            exercise_name = request.form.get("exercise_name")

            c.execute("""
                DELETE FROM user_exercises
                WHERE username = ? AND name = ?
            """, (user, exercise_name))

            db.commit()
            return redirect("/personalize")



    return render_template("personalize.html", user=user, food=food, exercise=exer)


@app.route("/results", methods=["GET","POST"])
def results():
    if "username" not in session:
        return redirect("/login")
    return render_template("results.html", params = ["calories", "fat", "sugar", "protein", "fiber", "cholesterol"], query = request.args['search_query'], foods = data.searchFood(request.args['search_query']))



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

def getFoodsList(criteria, data, params=()):
    DB_FILE = "static/food.db"
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    #conn.execute("PRAGMA foreign_keys = ON;")
    db = conn
    c = db.cursor()
    query = f"SELECT {data} FROM food WHERE {criteria}"
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
    app.debug = True
    app.run()
