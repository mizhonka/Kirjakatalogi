from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql:///mizhonka"
db=SQLAlchemy(app)

@app.route("/")
def index():
    sql=text("SELECT id, title, author FROM Books")
    result=db.session.execute(sql)
    books=result.fetchall()
    return render_template("index.html", books=books)

@app.route("/newbook")
def newbook():
    return render_template("newbook.html")

@app.route("/create", methods=["POST"])
def create():
    title=request.form["title"]
    author=request.form["author"]
    pub_year=request.form["pub_year"]
    lang=request.form["lang"]
    pagenumber=int(request.form["pagenumber"])
    genre=request.form.getlist("genre")
    sql=text("INSERT INTO books (title, author, pub_year, lang, pagenumber) VALUES (:title, :author, :pub_year, :lang, :pagenumber) RETURNING id")
    db.session.execute(sql, {"title":title, "author":author, "pub_year":pub_year, "lang":lang, "pagenumber":pagenumber})
    db.session.commit()
    return redirect("/")