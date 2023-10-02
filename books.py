import os
from db import db
from flask import session
from sqlalchemy.sql import text

def my_books():
    sql=text("SELECT b.id, b.title, b.author FROM Books b, Read r WHERE r.user_id=:id AND r.book_id=b.id")
    result=db.session.execute(sql, {"id":session["user_id"]})
    read_books=result.fetchall()
    return read_books

def create(title, author, pub_year, lang, pagenumber, genres):
    sql=text("INSERT INTO Books (title, author, pub_year, lang, pagenumber)" \
            "VALUES (:title, :author, :pub_year, :lang, :pagenumber) RETURNING id")
    result=db.session.execute(sql, {"title":title, "author":author, "pub_year":pub_year, "lang":lang, "pagenumber":pagenumber})
    book_id=result.fetchone()[0]
    for genre in genres:
        sql=text("INSERT INTO Genres (genre, book_id) VALUES (:genre, :book_id) RETURNING id")
        db.session.execute(sql, {"genre": genre, "book_id":book_id})
    db.session.commit()

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
    return [book, genres, is_read]

def mark_read(book_id):
    sql=text("INSERT INTO Read (book_id, user_id) VALUES (:book_id, :user_id)")
    db.session.execute(sql, {"book_id":book_id, "user_id":session["user_id"]})
    db.session.commit()

def mark_unread(book_id):
    sql=text("DELETE FROM Read WHERE book_id=:book_id AND user_id=:user_id")
    db.session.execute(sql, {"book_id":book_id, "user_id":session["user_id"]})
    db.session.commit()

def search_result(query, target):
    if target=="title":
        sql=text("SELECT id, title, author FROM Books WHERE title LIKE :query")
    elif target=="author":
        sql=text("SELECT id, title, author FROM Books WHERE author LIKE :query")
    else:
        sql=text("SELECT id, title, author FROM Books WHERE title LIKE :query OR author LIKE :query")
    result=db.session.execute(sql, {"query":"%"+query+"%"})
    results=result.fetchall()
    return results
