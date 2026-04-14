import csv
import sqlite3

data = sqlite3.connect('\static\food.db')

cursor = data.cursor()

create_table = '''CREATE TABLE food(
                name TEXT NOT NULL,
                calories INTEGER,
                fat REAL,
                sugar REAL,
                protein REAL,
                fiber REAL,
                cholesterol REAL);
                '''
cursor.execute(create_table)

file = open('../../foodone.csv')

contents = csv.reader(file)

insert_records = "INSERT INTO food (name, calories, fat, sugar, protein, fiber, cholesterol) VALUES(?, ?)"

cursor.executemany(insert_records, contents)

select_all = "SELECT * FROM food"

rows = cursor.execute(select_all).fetchall()

for r in rows:
    print(r)

connection.commit()
connection.close()
