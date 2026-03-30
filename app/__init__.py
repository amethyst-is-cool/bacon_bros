import sqlite3
import random
from flask import Flask, render_template
from flask import session, request, redirect

# Flask
app = Flask(__name__)
app.secret_key = 'secretkey'

# SQLite
DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

db.commit()
db.close()

@app.route('/', methods=["GET", "POST"])
def homepage():
    return render_template("home.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    return render_template("signup.html")

@app.route('/editinfo', methods=["GET", "POST"])
def editinfo():
    return render_template("edit_info.html")


# Flask
if __name__=='__main__':
    app.debug = False
    app.run()
