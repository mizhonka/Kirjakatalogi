import os
from db import db
from flask import session
from sqlalchemy import text

def add_review(score, review, book_id):
    r=get_review(book_id)
    if not r:
        sql=text("INSERT INTO Reviews(book_id, user_id, score, review) VALUES (:book_id, :user_id, :score, :review)")
    else:
        sql=text("UPDATE Reviews SET score=:score, review=:review WHERE book_id=:book_id AND user_id=:user_id")
    db.session.execute(sql, {"book_id":book_id, "user_id":session["user_id"], "score":score, "review":review})
    db.session.commit()

def get_my_score(book_id):
    sql=text("SELECT score FROM reviews WHERE book_id=:book_id AND user_id=:user_id")
    result=db.session.execute(sql, {"book_id":book_id, "user_id":session["user_id"]})
    return result.fetchone()

def get_average(book_id):
    sql=text("SELECT AVG(score) :: NUMERIC(10, 1) FROM Reviews WHERE book_id=:book_id")
    result=db.session.execute(sql, {"book_id":book_id})
    return result.fetchone()

def get_reviews(book_id):
    sql=text("SELECT r.id, r.user_id, r.score, r.review, u.username FROM Reviews r, Users u WHERE r.book_id=:book_id AND r.user_id=u.id")
    result=db.session.execute(sql, {"book_id":book_id})
    return result.fetchall()

def get_review(book_id):
    sql=text("SELECT score, review FROM Reviews WHERE book_id=:book_id AND user_id=:user_id")
    result=db.session.execute(sql, {"book_id":book_id, "user_id":session["user_id"]})
    return result.fetchone()

def delete_review(id):
    sql=text("DELETE FROM Reviews WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
