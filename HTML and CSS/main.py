from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/login")
def home():
    return render_template("login.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/seller")
def sell():
    return render_template("seller1.html")


@app.route("/buyer")
def buy():
    return "Welcome Buyer"
