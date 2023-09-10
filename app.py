from flask import Flask
from flask import render_template

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/newbook")
def newbook():
    return render_template("newbook.html")

@app.route("/create", methods=["ADD"])
def create():
    return redirect("/")