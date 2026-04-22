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
    height INT,
    sex TEXT,
    activity TEXT,
    loss REAL,
    burned REAL
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
    id INTEGER,
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
                "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    request.form["username"],
                    request.form["password"],
                    0,
                    0,
                    0,
                    "",
                    "",
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

    user = session["username"]

    d = True
    d2 = True

    food = fetch("user_foods", "username = ?", "name", (session["username"],))
    exer = fetch("user_exercises", "username = ?", "name", (session["username"],))


    sex = fetch("users", "username = ?", "sex", (session["username"],))[0][0]
    age = fetch("users", "username = ?", "age", (session["username"],))[0][0]
    height = fetch("users", "username = ?", "height", (session["username"],))[0][0]
    weight = fetch("users", "username = ?", "weight", (session["username"],))[0][0]
    act = fetch("users", "username = ?", "activity", (session["username"],))[0][0]



    exersL = []
    sts = []

    # for checking if BMI, etc. can be calculated

    if height != 0 and age != 0 and weight != 0 and act != "" and sex != "":
        haveInfo = True
        sts = statC(age, weight, height, sex, act)

        ex = fittedE(sex, sts[0], age, weight)[0]
        #sex, bmi, age, weight
        if len(ex) < 1:
            ex = [] #getExerList(True, "name", (), True)
        for i in range(1, len(ex)):
            exersL += [ex[i][0]]

    else:
        haveInfo = False

    values = nutDist(session["username"])


    #for dropdown

    foods = getFoodsList(True, "name")

    foodsL = []
    for i in range(1, len(foods)):
        foodsL += [foods[i][0]]




    if request.method == "POST":


        if "infoEdit" in request.form:
            return render_template("profile.html", user = user, d= False, d2 = haveInfo, food = food, exercises = exer, age = age, height = height, weight = weight,
            foods = foodsL, sex = sex, vals = values, activity = act, stats = sts)

        if "newInfo" in request.form:
            update_userinfo(session["username"], "age", request.form["age"])
            age = fetch("users", "username = ?", "age", (session["username"],))[0][0]
            update_userinfo(session["username"], "weight", request.form["weight"])
            weight = fetch("users", "username = ?", "weight", (session["username"],))[0][0]
            update_userinfo(session["username"], "height", request.form["height"])
            height = fetch("users", "username = ?", "height", (session["username"],))[0][0]
            update_userinfo(session["username"], "sex", request.form["sex"])
            sex = fetch("users", "username = ?", "sex", (session["username"],))[0][0]
            update_userinfo(session["username"], "activity", request.form["act"])
            act = fetch("users", "username = ?", "activity", (session["username"],))[0][0]
            if height != 0 and age != 0 and weight != 0 and act != "" and sex != "":
                haveInfo = True
                sts = statC(age, weight, height, sex, act)

                ex = fittedE(sex, sts[0], age, weight)[0]
                if len(ex) < 1:
                    ex = [] #getExerList(True, "name", (), True)

                #sex, bmi, age, weight
                for i in range(1, len(ex)):
                    exersL += [ex[i][0]]

            else:
                haveInfo = False
                sts = []
            return render_template("profile.html", user = user, d= True, d2 = haveInfo, food = food, exercises = exer, age = age, height = height, weight = weight,
            foods = foodsL, sex = sex, vals = values, activity = act, stats = sts, exers = exersL)

        #adding food
        if "ch" in request.form:
            choice = request.form["ch"]
            addFood(choice, session["username"])
            food = fetch("user_foods", "username = ?", "name", (session["username"],))
            values = nutDist(session["username"])
            return render_template("profile.html", user = user, d= True, d2 = haveInfo, food = food, exercises = exer, age = age, height = height, weight = weight,
            foods = foodsL, sex = sex, vals = values, activity = act, stats = sts, exers = exersL)

        #deleting food
        if "del" in request.form:
            choice = request.form["del"]
            deleteFood(choice, session["username"])
            values = nutDist(session["username"])
            food = fetch("user_foods", "username = ?", "name", (session["username"],))
            return render_template("profile.html", user = user, d= True, d2 = haveInfo, food = food, exercises = exer, age = age, height = height, weight = weight,
            foods = foodsL, sex = sex, vals = values, activity = act, stats = sts, exers = exersL)


        if "che" in request.form:
            choice = request.form["che"]
            ids = fittedE(sex, sts[0], age, weight)[1]
            addExer(choice, session["username"], ids)
            exer = fetch("user_exercises", "username = ?", "name", (session["username"],)) 

            return render_template("profile.html", user = user, d= True, d2 = haveInfo, food = food, exercises = exer, age = age, height = height, weight = weight, 
            foods = foodsL, sex = sex, vals = values, activity = act, stats = sts, exers = exersL)

        #deleting food
        if "dele" in request.form:
            choice = request.form["dele"]
            deleteExer(choice, session["username"])
            exer = fetch("user_exercises", "username = ?", "name", (session["username"],)) 

            return render_template("profile.html", user = user, d= True, d2 = haveInfo, food = food, exercises = exer, age = age, height = height, weight = weight,
            foods = foodsL, sex = sex, vals = values, activity = act, stats = sts, exers = exersL)


    return render_template("profile.html", user = user, d= True, d2 = haveInfo, food = food, exercises = exer, age = age, height = height, weight = weight,
    foods = foodsL, sex = sex, vals = values, activity = act, stats = sts, exers = exersL)


@app.route('/explore', methods=["GET", "POST"])
def explore():
    if "username" not in session:
        return redirect("/login")

    data = sqlite3.connect('static/workout.db')
    cursor = data.cursor()

    cursor.execute("""
        SELECT age, gender, weight, workout 
        FROM workouts
    """)

    rows = cursor.fetchall()
    data.close()

    male = []
    female = []

    for row in rows:
        age = row[0]
        gender = str(row[1]).strip().lower()
        weight = row[2]
        workout = row[3]

        try:
            age = float(age)
            weight = float(weight)

            # Skip invalid values
            if age <= 0 or weight <= 0:
                continue

        except (ValueError, TypeError):
            continue

        point = {
            "x": age,
            "y": weight,
            "label": workout
        }

        if gender == "male":
            male.append(point)
        elif gender == "female":
            female.append(point)

    return render_template("explore.html", male=male, female=female)


#personalize is responsible for displaying info about your food and exerc preferences
@app.route('/personalize', methods=["GET", "POST"])
def personalize():
    if "username" not in session:
        return redirect("/login")

    sex = fetch("users", "username = ?", "sex", (session["username"],))[0][0]
    age = fetch("users", "username = ?", "age", (session["username"],))[0][0]
    height = fetch("users", "username = ?", "height", (session["username"],))[0][0]
    weight = fetch("users", "username = ?", "weight", (session["username"],))[0][0]
    act = fetch("users", "username = ?", "activity", (session["username"],))[0][0]
    burned = fetch("users", "username = ?", "burned", (session["username"],))[0][0]

    values = nutDist(session["username"])

    food = fetch("user_foods", "username = ?", "name", (session["username"],))
    exercises = fetch("user_exercises", "username = ?", "name, session_duration, calories_burned", (session["username"],))

    exercise = []
    for i in range(len(exercises)):
        exercise += [exercises[i][0]]

    

    if len(values) > 0:
        total = values[0]
    else:
        total = 0


    if height != 0 and age != 0 and weight != 0 and act != "" and sex != "":
        sts = statC(age, weight, height, sex, act)
        tdee = sts[3]
    else:
        total = 0
        tdee = 0

    loss = fetch("users", "username = ?", "loss", (session["username"],))

    x = eStats(session["username"])
    
    if request.method == 'POST':
        if 'pound' in request.form:
            addLoss(request.form["pound"], session["username"])

    

    
    return render_template("personalize.html", food = food, exercise = exercise, total = total, tdee = tdee, loss = loss, workout = burned, x = x)


@app.route("/results", methods=["GET","POST"])
def results():
    if "username" not in session:
        return redirect("/login")
    #print(data.searchFood(request.args['search_query']))
    return render_template("results.html", params = ["calories", "fat", "sugar", "protein", "fiber", "cholesterol"], query = request.args['search_query'], foods = data.searchFood(request.args['search_query']))



@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/login")

def addLoss(pound, user):
    db = get_db()
    c = db.cursor()
    pound = float(pound)
    query = "UPDATE users SET loss = ? WHERE username = ?"
    params = (pound, user)
    c.execute(query, params)
    db.commit()
    db.close()
    return True

def addFood(foodName, user):
    db = get_db()
    c = db.cursor()
    n = getFoodsList("name = ?", "*", (foodName,))
    query = "INSERT INTO user_foods (username, name, calories, fat, sugar, protein, fiber, cholesterol) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    params = (user, foodName, n[0][1], n[0][2], n[0][3], n[0][4], n[0][5], n[0][6])
    c.execute(query, params)
    db.commit()
    db.close()
    return True

def deleteFood(foodName, user):
    db = get_db()
    c = db.cursor()
    query = "DELETE FROM user_foods WHERE username = ? AND name = ? LIMIT 1"
    params = (user, foodName)
    c.execute(query, params)
    db.commit()
    db.close()
    return True

def addExer(name, user, ids):
    db = get_db()
    c = db.cursor()
    i = ",".join(["?"] * len(ids))
    q = f"name = ? AND id IN ({i}) LIMIT 1"
    params = tuple([name] + ids)
    n = getExerList(q, "*", params, False)
    print(n)
    #id|age|gender|weight|height|session_duration|calories_burned|workout_type|BMI|name|sets|reps|benefit|burns_calories|target_muscle_group|workout
    #username, age, gender, weight, height, session_duration, calories_burned, workout_type, BMI, name, sets, reps, benefit, burns_calories, target_muscle_group, workout 
    query = "INSERT INTO user_exercises (id, username, age, gender, weight, height, session_duration, calories_burned, workout_type, BMI, name, sets, reps, benefit, burns_calories, target_muscle_group, workout) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    params = (n[0][0], user, n[0][1], n[0][2], n[0][3], n[0][4], n[0][5], n[0][6], n[0][7], n[0][8], n[0][9], n[0][10], n[0][11], n[0][12], n[0][13], n[0][14], n[0][15])
    c.execute(query, params)
    db.commit()
    db.close()
    return True

def deleteExer(name, user):
    db = get_db()
    c = db.cursor()
    query = "DELETE FROM user_exercises WHERE username = ? AND name = ? LIMIT 1"
    params = (user, name)
    c.execute(query, params)
    db.commit()
    db.close()
    return True

def fetch(table, criteria, data, params=()):
    db = get_db()
    c = db.cursor()
    query = f"SELECT {data} FROM {table} WHERE {criteria}"
    c.execute(query, params)
    data = c.fetchall()
    db.commit()
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
    db.commit()
    db.close()
    return data

def getExerList(criteria, data, params=(), cleaned=False):
    DB_FILE = "static/workout.db"
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    #conn.execute("PRAGMA foreign_keys = ON;")
    db = conn
    c = db.cursor()
    if cleaned:
        query = f"SELECT DISTINCT {data} FROM workouts WHERE {criteria}"
    else:
        print("Getiing one")
        print(criteria)
        print(params)
        query = f"SELECT {data} FROM workouts WHERE {criteria}"

    c.execute(query, params)
    data = c.fetchall()
    db.commit()
    db.close()
    return data

def fittedE(sex, bmi, age, weight):
    #gender, BMI, age, weight
    weight = weight * 0.453592
    al = getExerList("gender = ? AND age BETWEEN (? - 5) AND (? + 5) AND BMI BETWEEN (? - 2) AND (? + 2) AND weight BETWEEN (? - 5) AND (? + 5)", "name", (sex, age, age, bmi, bmi, weight, weight), True)
    ind = getExerList("gender = ? AND age BETWEEN (? - 5) AND (? + 5) AND BMI BETWEEN (? - 2) AND (? + 2) AND weight BETWEEN (? - 5) AND (? + 5)", "id", (sex, age, age, bmi, bmi, weight, weight), True)
    
    i = []
    for d in ind:
        i += [d[0]]
    print(i)
    return [al, i]
    

def update_userinfo(user, kind, info):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(f"UPDATE users SET {kind} = ? WHERE username=?", (info, user))
    db.commit()
    db.close()

def nutDist(user):
    vls = []
    nutrients = ['calories', 'fat', 'cholesterol', 'sugar', 'fiber', 'protein']
    for i in nutrients:
        sm = 0
        lst = fetch("user_foods", "username = ?", i, (user,))
        for l in lst:
            sm += l[0]
        vls += [sm]
    return vls

def statC(age, weight, height, sex, act):
    l = []
    status = ""
    bmi = (weight / (height**2)) * 702

    if bmi < 18.5:
        status = "Underweight"
    elif bmi < 24.9:
        status = "Normal"
    elif bmi < 29.9:
        status = "Overweight"
    elif bmi >= 30:
        status = "Obese"


    kgW = 0.453592 * weight
    cmH = 2.54 * height

    
    if sex == "Male":
        bmr = (10 * kgW) + (6.25 * cmH) - (5 * age) + 5
    if sex == "Female":
        bmr = (10 * kgW) + (6.25 * cmH) - (5 * age) -161
    elif sex != "Female" and sex != "Male":
        bmr = (((10 * kgW) + (6.25 * cmH) - (5 * age) + 5) + ((10 * kgW) + (6.25 * cmH) - (5 * age) -161)) / 2

    if act == "Sedentary":
        tdee = bmr * 1.2
    if act == "Lightly Active":
        tdee = bmr * 1.375
    if act == "Moderately Active":
        tdee = bmr * 1.55
    if act == "Very Active":
        tdee = bmr * 1.725
    if act == "Extra Active":
        tdee = bmr * 1.9

    l = [round(bmi, 2), status, round(bmr, 2), round(tdee, 2)]
    return l


def eStats(user):
    wrks = fetch("user_exercises", "username = ?", "name, session_duration, calories_burned, reps, sets", (user,))
    x = []
    for w in wrks:
        name = w[0]
        dur = w[1] * 60
        cals = w[2]
        reps = (w[3] * w[4])
        x.append({
            "name": name + " " + str(round(cals/dur)) + " cals/min",
            "reps": reps / dur,
            "cals": cals / dur
        })
    return x

# Flask
if __name__=='__main__':
    app.debug = False
    app.run()
