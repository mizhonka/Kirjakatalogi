from os import getenv
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash

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

@app.route("/login", methods=["POST"])
def login():
    username=request.form["username"]
    password=request.form["password"]
    sql=text("SELECT id, password, is_admin FROM Users WHERE username=:username")
    result=db.session.execute(sql, {"username":username})
    user=result.fetchone()
    if not user:
        return render_template("error.html", error="Käyttäjätunnus tai salasana on väärin!")
    hash_value=user.password
    if check_password_hash(hash_value, password):
        session["username"]=username
        session["user_id"]=user.id
        session["is_admin"]=user.is_admin
        return redirect("/")
    return render_template("error.html", error="Käyttäjätunnus tai salasana on väärin!")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/newuser", methods=["POST"])
def newuser():
    username=request.form["username"]
    if len(username)>30:
        return render_template("error.html", error="Käyttäjänimi on liian pitkä!")
    password=request.form["password"]
    if len(username)<1 or len(password)<1:
        return render_template("error.html", error="Täytä kaikki kentät!")
    hash_value=generate_password_hash(password)
    sql=text("INSERT INTO Users (username, password, is_admin) VALUES (:username, :password, :is_admin)")
    is_admin=False
    if username=="admin":
        is_admin=True
    try:
        db.session.execute(sql, {"username":username, "password":hash_value, "is_admin":is_admin})
    except:
        return render_template("error.html", error="Tili tällä käyttäjänimellä on jo olemassa!")
    db.session.commit()
    return render_template("createduser.html")

@app.route("/logout")
def logout():
    del session["username"]
    del session["is_admin"]
    del session["user_id"]
    return redirect("/")

@app.route("/newbook")
def newbook():
    return render_template("newbook.html")

@app.route("/create", methods=["POST"])
def create():
    title=request.form["title"]
    if len(title)<1:
        return render_template("error.html", error="Täytäthän kaikki pakolliset kentät!")
    if len(title)>200:
        return render_template("error.html", error="Kirjan nimi on liian pitkä!")
    author=request.form["author"]
    if len(author)<1:
        return render_template("error.html", error="Täytäthän kaikki pakolliset kentät!")
    if len(author)>200:
        return render_template("error.html", error="Kirjailijan nimi on liian pitkä!")
    pub_year_str=request.form["pub_year"]
    if len(pub_year_str)<1:
        return render_template("error.html", error="Täytäthän kaikki pakolliset kentät!")
    try:
        pub_year=int(pub_year_str)
    except:
        return render_template("error.html", error="Ilmestymisvuoden on oltava numeroarvo!")
    lang=request.form["lang"]
    pagenumber_str=request.form["pagenumber"]
    if len(pagenumber_str)<1:
        return render_template("error.html", error="Täytäthän kaikki pakolliset kentät!")
    try:
        pagenumber=int(pagenumber_str)
    except:
        return render_template("error.html", error="Sivumäärän on oltava numeroarvo!")
    genres=request.form.getlist("genre")
    sql=text("INSERT INTO Books (title, author, pub_year, lang, pagenumber)" \
            "VALUES (:title, :author, :pub_year, :lang, :pagenumber) RETURNING id")
    result=db.session.execute(sql, {"title":title, "author":author, "pub_year":pub_year, "lang":lang, "pagenumber":pagenumber})
    book_id=result.fetchone()[0]
    for genre in genres:
        sql=text("INSERT INTO Genres (genre, book_id) VALUES (:genre, :book_id) RETURNING id")
        db.session.execute(sql, {"genre": genre, "book_id":book_id})
    db.session.commit()
    return redirect("/")

@app.route("/book_page/<int:id>")
def book_page(id):
    sql=text("SELECT title, author, pub_year, lang, pagenumber FROM Books WHERE id=:id")
    result=db.session.execute(sql, {"id":id})
    book=result.fetchone()
    sql=text("SELECT genre FROM Genres WHERE book_id=:id")
    result=db.session.execute(sql, {"id":id})
    genres=result.fetchall()
    sql=text("SELECT id FROM Read WHERE book_id=:id AND user_id=:user_id")
    result=db.session.execute(sql, {"id":id, "user_id":session["user_id"]}).fetchone()
    is_read=False
    if result:
        is_read=True
    return render_template("book.html", book=book, genres=genres, book_id=id, is_read=is_read)

@app.route("/mark_read", methods=["POST"])
def mark_read():
    book_id=request.form["book_id"]
    sql=text("INSERT INTO Read (book_id, user_id) VALUES (:book_id, :user_id)")
    db.session.execute(sql, {"book_id":book_id, "user_id":session["user_id"]})
    db.session.commit()
    route="/book_page/"+str(book_id)
    return redirect(route)

@app.route("/mark_unread", methods=["POST"])
def mark_unread():
    book_id=request.form["book_id"]
    sql=text("DELETE FROM Read WHERE book_id=:book_id AND user_id=:user_id")
    db.session.execute(sql, {"book_id":book_id, "user_id":session["user_id"]})
    db.session.commit()
    route="/book_page/"+str(book_id)
    return redirect(route)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/search_result", methods=["GET"])
def search_result():
    query=request.args["query"]
    target=request.args["target"]
    if target=="title":
        sql=text("SELECT id, title, author FROM Books WHERE title LIKE :query")
    elif target=="author":
        sql=text("SELECT id, title, author FROM Books WHERE author LIKE :query")
    else:
        sql=text("SELECT id, title, author FROM Books WHERE title LIKE :query OR author LIKE :query")
    result=db.session.execute(sql, {"query":"%"+query+"%"})
    results=result.fetchall()
    return render_template("search.html", results=results)
