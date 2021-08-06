from os import environ

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from json import loads, dumps
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    "Show portfolio of stocks"

    stocks = []

    for stock, amount in loads(
        db.execute("SELECT stocks FROM users WHERE id = ?", session["user_id"])[0][
            "stocks"
        ]
    ).items():
        quote = lookup(stock)
        quote["amount"] = amount
        stocks.append(quote)

    return render_template("index.html", stocks=stocks)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    "Buy shares of stock"
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a number")
        if not quote:
            return apology("unknown stock symbol")
        elif shares <= 0:
            return apology("shares must be a positive number")

        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
        cash = user["cash"] - quote["price"] * shares
        if cash < 0:
            return apology("you don't have enough money")
        currentStocks = loads(user["stocks"])
        currentTransactions = loads(user["transactions"])
        try:
            currentStocks[quote["symbol"]] += shares
            currentTransactions.append(
                {
                    "symbol": quote["symbol"],
                    "transaction": f"-{quote['price'] * shares}",
                    "money": cash,
                    "date": str(datetime.now()),
                }
            )
        except:
            currentStocks[quote["symbol"]] = shares
            currentTransactions.append(
                {
                    "symbol": quote["symbol"],
                    "transaction": f"-{quote['price'] * shares}",
                    "money": cash,
                    "date": str(datetime.now()),
                }
            )

        db.execute(
            "UPDATE users SET cash = ?, stocks = ?, transactions = ? WHERE id = ?",
            cash,
            dumps(currentStocks),
            dumps(currentTransactions),
            session["user_id"],
        )
        return render_template(
            "buy.html",
            companyName=quote["name"],
            money=cash,
            spent=quote["price"] * shares,
        )
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    "Show history of transactions"
    transactions = sorted(
        loads(
            db.execute(
                "SELECT transactions FROM users WHERE id = ?", session["user_id"]
            )[0]["transactions"]
        ),
        key=lambda x: x["date"],
        reverse=True,
    )
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    "Log user in"

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT hash, id FROM users WHERE username = ?",
            request.form.get("username"),
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    "Log user out"

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    "Get stock quote."
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("unknown stock symbol")
        return render_template(
            "quote.html", stockPrice=quote["price"], companyName=quote["name"]
        )

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    "Register user"
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Forget any user_id
        session.clear()

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not bool(username) or not bool(password):
            return apology("invalid username and/or password")
        elif confirmation != password:
            return apology("passwords don't match")
        else:
            try:
                db.execute(
                    "INSERT INTO users (username, hash, stocks) VALUES (?, ?, ?)",
                    username,
                    generate_password_hash(password),
                    "{}",
                )
                # Remember which user has logged in
                session["user_id"] = db.execute(
                    "SELECT id FROM users WHERE username = ?", username
                )[0]["id"]
            except ValueError:
                return apology("username already taken")
            return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    "Sell shares of stock"
    if request.method == "POST":
        if request.form.get("symbol") == None:
            return apology("please select a symbol")
        quote = lookup(request.form.get("symbol"))
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a number")
        if not quote:
            return apology("unknown stock symbol")
        elif shares <= 0:
            return apology("shares must be a positive number")
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
        cash = user["cash"] + quote["price"] * shares
        currentStocks = loads(user["stocks"])
        currentTransactions = loads(user["transactions"])
        try:
            currentStocks[quote["symbol"]] -= shares
            currentTransactions.append(
                {
                    "symbol": quote["symbol"],
                    "transaction": f"+{quote['price'] * shares}",
                    "money": cash,
                    "date": str(datetime.now()),
                }
            )
            if currentStocks[quote["symbol"]] < 0:
                return apology("you don't have that stock")
            elif currentStocks[quote["symbol"]] == 0:
                del currentStocks[quote["symbol"]]
        except:
            return apology("you don't have that stock")

        db.execute(
            "UPDATE users SET cash = ?, stocks = ? WHERE id = ?",
            cash,
            dumps(currentStocks),
            session["user_id"],
        )
        return render_template(
            "sell.html",
            companyName=quote["name"],
            money=cash,
            spent=quote["price"] * shares,
        )
    stocks = loads(
        db.execute("SELECT stocks FROM users WHERE id = ?", session["user_id"])[0][
            "stocks"
        ]
    )
    return render_template("sell.html", stocks=stocks.keys())


def errorhandler(e):
    "Handle error"
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
