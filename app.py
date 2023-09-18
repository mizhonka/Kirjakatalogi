from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

app=Flask(__name__)
app.secret_key=getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"]=getenv("DATABASE_URL")
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
    genres=request.form.getlist("genre")
    sql=text("INSERT INTO Books (title, author, pub_year, lang, pagenumber) VALUES (:title, :author, :pub_year, :lang, :pagenumber) RETURNING id")
    result=db.session.execute(sql, {"title":title, "author":author, "pub_year":pub_year, "lang":lang, "pagenumber":pagenumber})
    book_id=result.fetchone()[0]
    for genre in genres:
        sql=text("INSERT INTO Genres (genre, book_id) VALUES (:genre, :book_id) RETURNING id")
        db.session.execute(sql, {"genre": genre, "book_id":book_id})
    db.session.commit()
    return redirect("/")

@app.route("/book_page/<int:id>")
def book_page(id):
    sql=text("SELECT title, author, pub_year, lang, pagenumber, genre FROM Books WHERE id=:id")
    result=db.session.execute(sql, {"id":id})
    book=result.fetchone()
    sql=text("SELECT genre FROM Genres WHERE book_id=:id")
    result=db.session.execute(sql, {"id":id})
    genres=result.fetchall()
    return render_template("book.html", book=book, genres=genres)