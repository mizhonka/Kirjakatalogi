from app import app
from flask import redirect, render_template, request, session
import users
import books
import reviews

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/review", methods=["POST"])
def review():
    title=request.form["title"]
    book_id=request.form["book_id"]
    r=reviews.get_review(book_id)
    if r:
        cur_score=r.score
        cur_review=r.review
    else:
        cur_score=1
        cur_review=""
    return render_template("review.html", title=title, book_id=book_id, cur_score=cur_score, cur_review=cur_review)

@app.route("/add_review", methods=["POST"])
def add_review():
    score=request.form["score"]
    review=request.form["review"]
    book_id=request.form["book_id"]
    reviews.add_review(score, review, book_id)
    route="/book_page/"+str(book_id)
    return redirect(route)

@app.route("/delete_review", methods=["POST"])
def delete_review():
    id=request.form["id"]
    book_id=request.form["book_id"]
    reviews.delete_review(id)
    route="/book_page/"+str(book_id)
    return redirect(route)

@app.route("/my_books")
def my_books():
    read_books=books.my_books()
    return render_template("my_books.html", books=read_books)

@app.route("/login", methods=["POST"])
def login():
    username=request.form["username"]
    password=request.form["password"]
    if not users.login(username, password):
        return render_template("error.html", error="Käyttäjätunnus tai salasana on väärin!")
    return redirect("/")

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
    if not users.newuser(username, password):
        return render_template("error.html", error="Käyttäjätili tällä tunnuksella on jo olemassa!")
    return render_template("createduser.html")

@app.route("/logout")
def logout():
    users.logout()
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
    books.create(title, author, pub_year, lang, pagenumber, genres)
    return redirect("/")

@app.route("/book_page/<int:id>")
def book_page(id):
    info=books.book_page(id)
    score=reviews.get_average(id)
    r=reviews.get_reviews(id)
    if score:
        score=score[0]
    my_score=reviews.get_my_score(id)
    if my_score:
        my_score=my_score[0]
    return render_template("book.html", book=info[0], genres=info[1], book_id=id, is_read=info[2], score=score, my_score=my_score, reviews=r)

@app.route("/mark_read", methods=["POST"])
def mark_read():
    book_id=request.form["book_id"]
    books.mark_read(book_id)
    route="/book_page/"+str(book_id)
    return redirect(route)

@app.route("/mark_unread", methods=["POST"])
def mark_unread():
    book_id=request.form["book_id"]
    books.mark_unread(book_id)
    route="/book_page/"+str(book_id)
    return redirect(route)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/search_result", methods=["GET"])
def search_result():
    query=request.args["query"]
    target=request.args["target"]
    results=books.search_result(query, target)
    return render_template("search.html", results=results)
