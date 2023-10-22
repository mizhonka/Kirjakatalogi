import os
from db import db
from flask import session
from sqlalchemy import text


def lang_query(lng):
    return "SELECT COUNT(*) FROM Books b, Read r WHERE r.user_id=:id AND r.book_id=b.id AND b.lang=" + "'" + lng + "'"


def genre_query(genre):
    return "SELECT COUNT(*) FROM Genres g, Read r WHERE r.user_id=:id AND r.book_id=g.book_id AND g.genre="+"'"+genre+"'"


def execute_with_id(sql, id):
    return db.session.execute(sql, {"id": id}).fetchone()[0]


def get_basic_stats(id):
    sql = text("SELECT COUNT(*) FROM Read WHERE user_id=:id")
    n_books = execute_with_id(sql, id)
    sql = text(
        "SELECT SUM(b.pagenumber) FROM Read r, Books b WHERE r.user_id=:id AND r.book_id=b.id")
    n_pages = execute_with_id(sql, id)
    if not n_pages:
        n_pages = 0
    return [n_books, n_pages]


def get_lang_stats(id):
    total = get_basic_stats(id)[0]
    sql = text(lang_query("suomi"))
    n_fin = execute_with_id(sql, id)
    if not n_fin == 0:
        fin_per = round(n_fin/total*100)
    else:
        fin_per = 0
    sql = text(lang_query("englanti"))
    n_eng = execute_with_id(sql, id)
    if not n_eng == 0:
        eng_per = round(n_eng/total*100)
    else:
        eng_per = 0
    sql = text(lang_query("ruotsi"))
    n_sv = execute_with_id(sql, id)
    if not n_sv == 0:
        sv_per = round(n_sv/total*100)
    else:
        sv_per = 0
    return [(n_fin, fin_per), (n_eng, eng_per), (n_sv, sv_per)]


def get_genre_stats(id):
    total = get_basic_stats(id)[0]
    genres = ["Lapset", "Jännitys", "Mysteeri", "Klassikko",
              "Kauhu", "Fantasia", "Scifi", "Romantiikka"]
    n_genres = []
    for g in genres:
        sql = text(genre_query(g))
        n_genre = execute_with_id(sql, id)
        if not n_genre == 0:
            n_genres.append((n_genre, round(n_genre/total*100)))
        else:
            n_genres.append((n_genre, 0))
    return n_genres
