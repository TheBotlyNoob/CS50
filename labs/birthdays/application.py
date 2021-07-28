from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from dotenv import load_env

# Load a .env file
load_env()

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        name = request.form.get('name')
        month = request.form.get('month')
        day = request.form.get('day')

        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

        return redirect("/")

    else:

        html = ''

        for bday in db.execute('SELECT * FROM birthdays'):
            html += f'''
                        <tr>
                            <td>{bday['name']}</td>
                            <td>{bday['month']}/{bday['day']}</td>
                        </tr>
                    '''

        return render_template("index.html", bdays=html)