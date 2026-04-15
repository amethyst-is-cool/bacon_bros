import csv
import sqlite3


# if __name__  == "__main__":
#     data = sqlite3.connect('static/food.db')
#
#     cursor = data.cursor()
#
#     create_table = '''CREATE TABLE IF NOT EXISTS food(
#                     name TEXT NOT NULL,
#                     calories INTEGER,
#                     fat REAL,
#                     sugar REAL,
#                     protein REAL,
#                     fiber REAL,
#                     cholesterol REAL);
#                     '''
#     cursor.execute(create_table)
#
#     files = ['../../foodone.csv', '../../foodtwo.csv', '../../foodthree.csv', '../../foodfour.csv', '../../foodfive.csv']
#     for i in range(5):
#         file = open(files[i])
#
#         contents = csv.reader(file)
#         for row in contents:
#             row = row[2:5] + row[9:13]
#             cursor.execute("INSERT INTO food (name, calories, fat, sugar, protein, fiber, cholesterol) VALUES(?, ?, ? ,?, ?, ?, ?)", row)
#         # assert False
#         #
#         # insert_records = "INSERT INTO food (name, calories, fat, sugar, protein, fiber, cholesterol) VALUES(?, ?)"
#         #
#         # cursor.executemany(insert_records, contents)
#
#         select_all = "SELECT * FROM food"
#
#         rows = cursor.execute(select_all).fetchall()
#
#         for r in rows:
#             print(r)
#
#     data.commit()
#     data.close()

def searchFood(food):
    data = sqlite3.connect('static/food.db')
    cursor = data.cursor()

    cursor.execute("SELECT * FROM food WHERE name = ?", (food, ))
    return cursor.fetchone()

print(searchFood("cream cheese fat free"))
