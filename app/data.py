import csv
import sqlite3


def csvParse():
    data = sqlite3.connect('static/workout.db')

    cursor = data.cursor()

    create_table = """
        CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        workout TEXT)
    """

    cursor.execute(create_table)

    file = open("../../workout.csv")

    contents = csv.reader(file)
    r = 0
    for row in contents:
        row = [r] + row[0:4] + row[7:10] + [row[14]] + row[32:38] + [row[42]]
        cursor.execute("INSERT INTO workouts (id, age, gender, weight, height, session_duration, calories_burned, workout_type, BMI, name, sets, reps, benefit, burns_calories, target_muscle_group, workout) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
        r += 1
    # assert False
    #
    # insert_records = "INSERT INTO food (name, calories, fat, sugar, protein, fiber, cholesterol) VALUES(?, ?)"
    #
    # cursor.executemany(insert_records, contents)

    select_all = "SELECT * FROM workouts"

    rows = cursor.execute(select_all).fetchall()

    for r in rows:
        print(r)

    data.commit()
    data.close()

# csvParse()

def searchFood(food):
    data = sqlite3.connect('static/food.db')
    cursor = data.cursor()

    cursor.execute("SELECT * FROM food WHERE name LIKE ?", ('%'+food+'%', ))
    x = cursor.fetchall()
    if len(x)>5:
        return x[0:5]
    return x


def searchWorkout(id):
    data = sqlite3.connect('static/workout.db')
    cursor = data.cursor()

    cursor.execute("SELECT * FROM workouts WHERE id = ?", (id, ))
    x = cursor.fetchall()
    return x

#print(searchWorkout(1))