import os

import requests
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from helpers import apology, login_required, lookup, usd
import math

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
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

API_KEY = os.environ.get("API_KEY")

@app.route("/")
@login_required
def index():
    rows = db.execute("SELECT stock , sum(quantity) quantity FROM stock WHERE username = :id group by stock having sum(quantity)>0" ,
                        id=session["user_id"] )
    return render_template("index.html" , rows = rows)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    base_URL = "https://cloud.iexapis.com/stable/stock/"


    rows = db.execute("SELECT * FROM users WHERE id = :id",
                        id=session["user_id"])

    cash = rows[0]["cash"]

    if request.method == "POST":
        base_URL = "https://cloud.iexapis.com/stable/stock/"
        symbol = request.form.get("symbol") + "/quote?token="
        URL = base_URL + symbol + API_KEY

        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)
        elif not requests.get(URL):
            return apology("invalid symbol", 403)

        # Ensure password was submitted
        elif not request.form.get("quantity"):
            return apology("must provide quantity", 403)


        else:
            data = requests.get(URL).json()
            if data["latestPrice"] * int(request.form.get("quantity")) > cash:
                return apology("cash is not enough", 403)
            else:

                db.execute("UPDATE users SET cash = :cash WHERE id = :id",
                            id=session["user_id"] ,cash = cash- data["latestPrice"] * int(request.form.get("quantity")))

                db.execute("INSERT INTO stock (buy , username, date, stock, price , quantity) VALUES ( :buy , :id, :date, :stock, :price , :quantity)",
                            buy = 1, id = session["user_id"]  , date = date.today() , stock = request.form.get("symbol"), price = data["latestPrice"] , quantity = request.form.get("quantity") )

                status = 1
                return render_template("buy.html" , status = status)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    rows = db.execute("select * from stock  WHERE username = :id",
                id=session["user_id"] )
    return render_template("history.html" , rows = rows)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """register user"""

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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) == 1 :
            return apology("username exists", 403)

        row_id = db.execute("SELECT count(*) as num FROM users")[0]["num"]
        db.execute("INSERT INTO users (id , username , hash) VALUES ( :id , :username , :hash)",
                    id = row_id+1 , username =request.form.get("username") , hash = generate_password_hash(request.form.get("password")) )

        # Remember which user has logged in
        rows_after = db.execute("SELECT * FROM users WHERE username = :username",
                                username=request.form.get("username"))
        session["user_id"] = rows_after[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")




@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET"])
@login_required
def quote():
    return render_template("quote.html")
    """Get stock quote."""

@app.route("/quote/<quote>", methods=["POST"])
@login_required
def quote_p(quote):
        base_URL = "https://cloud.iexapis.com/stable/stock/"
        symbol = quote + "/quote?token="
        URL = base_URL + symbol + API_KEY


        if not requests.get(URL):
            return '1'
        else :
            data = requests.get(URL).json()
            return data

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    base_URL = "https://cloud.iexapis.com/stable/stock/"




    if request.method == "POST":

        rows_buy = db.execute("SELECT * FROM stock WHERE username = :id and buy =1 and stock = :stock",
                        id=session["user_id"] , stock = request.form.get("symbol") )

        rows_sell = db.execute("SELECT * FROM stock WHERE username = :id and buy =0 and stock = :stock",
                        id=session["user_id"] , stock = request.form.get("symbol") )
        rows = db.execute("SELECT * FROM users WHERE id = :id",
                          id=session["user_id"])

        cash = rows[0]["cash"]

        if rows_buy:
            if rows_sell:
                quantity = rows_buy[0]["quantity"] - rows_sell[0]["quantity"]
            else:
                quantity = rows_buy[0]["quantity"]

        base_URL = "https://cloud.iexapis.com/stable/stock/"
        symbol = request.form.get("symbol") + "/quote?token="
        URL = base_URL + symbol + API_KEY
        data = requests.get(URL).json()



        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)

        # Ensure password was submitted
        elif not request.form.get("quantity"):
            return apology("must provide quantity", 403)

        elif not rows_buy or quantity == 0 :
            return apology("you don't have the stock", 403)

        elif quantity - int(request.form.get("quantity")) < 0 :
            return apology("you don't have enough stock", 403)


        else:
            db.execute("UPDATE users SET cash = :cash WHERE id = :id",
                        id=session["user_id"] ,cash = cash + data["latestPrice"] * int(request.form.get("quantity")))

            db.execute("INSERT INTO stock (buy , username, date, stock, price , quantity) VALUES ( :buy , :id, :date, :stock, :price , :quantity)",
                        buy = 0, id = session["user_id"]  , date = date.today() , stock = request.form.get("symbol"), price = data["latestPrice"] , quantity = int(request.form.get("quantity")) * -1 )

            status = 1
            return render_template("sell.html" , status = status)
    else:
        return render_template("sell.html")


@app.route("/price/<quote>", methods=["POST"])
def price(quote):
    base_URL = "https://cloud.iexapis.com/stable/stock/"
    symbol = quote + "/chart/5d?token="
    URL = base_URL + symbol + API_KEY
    data = requests.get(URL).json()
    return jsonify(data)

@app.route("/position", methods=["POST"])
def position():
    rows = db.execute("SELECT stock ,sum(quantity) quantity, sum(quantity*price) total FROM stock WHERE username = :id group by stock having sum(quantity) > 0 ",
                        id=session["user_id"] )
    rows2 = db.execute("SELECT * FROM users WHERE id = :id",
                          id=session["user_id"])

    x= {"cash": 'cash', "total" : math.ceil(rows2[0]["cash"])}
    print(x)
    rows.append(x)
    print(rows)





    return jsonify(rows)

@app.route("/sellall/<quote>", methods=[ "POST"])
@login_required
def sellall(quote):
    base_URL = "https://cloud.iexapis.com/stable/stock/"

    if request.method == "POST":

        rows_buy = db.execute("SELECT sum(quantity) quantity FROM stock WHERE username = :id and buy =1 and stock = :stock group by stock" ,
                        id=session["user_id"] , stock = quote )

        rows_sell = db.execute("SELECT sum(quantity) quantity FROM stock WHERE username = :id and buy =0 and stock = :stock group by stock",
                        id=session["user_id"] , stock = quote )
        rows = db.execute("SELECT * FROM users WHERE id = :id",
                          id=session["user_id"])

        cash = rows[0]["cash"]

        if rows_buy:
            if rows_sell:
                quantity = rows_buy[0]["quantity"] - rows_sell[0]["quantity"]
            else:
                quantity = rows_buy[0]["quantity"]

        base_URL = "https://cloud-sse.iexapis.com/stable/stock/"
        symbol = quote + "/quote?token="
        URL = base_URL + symbol + API_KEY
        data = requests.get(URL).json()

        db.execute("UPDATE users SET cash = :cash WHERE id = :id",
                    id=session["user_id"] ,cash = cash + data["latestPrice"] * int(quantity))

        db.execute("INSERT INTO stock (buy , username, date, stock, price , quantity) VALUES ( :buy , :id, :date, :stock, :price , :quantity)",
                    buy = 0, id = session["user_id"]  , date = date.today() , stock = quote, price = data["latestPrice"] , quantity = int(quantity) * -1 )

        status = "SUCCESS"
        return "SUCCESS"

@app.route("/perf/<range>", methods = ['POST'])
@login_required
def perf(range):
    if range != '0' :
        rows = db.execute("select * from performance  WHERE id = :id and date > date('now', :range) order by datetime(date) asc" ,
                    id=session["user_id"] , range = '-' + range+ ' ' + 'month' )
        print ('-' + range + ' ' + 'month' )
    else:
        rows = db.execute("select * from performance  WHERE id = :id order by datetime(date) asc" ,
        id=session["user_id"] )
    return jsonify(rows)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
