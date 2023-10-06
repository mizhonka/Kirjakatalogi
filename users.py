import os
from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex


def newuser(username, password):
    hash_value = generate_password_hash(password)
    sql = text(
        "INSERT INTO Users (username, password, is_admin) VALUES (:username, :password, :is_admin)")
    is_admin = False
    if username == "admin":
        is_admin = True
    try:
        db.session.execute(
            sql, {"username": username, "password": hash_value, "is_admin": is_admin})
    except:
        return False
    db.session.commit()
    return True


def login(username, password):
    sql = text("SELECT id, password, is_admin FROM Users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    hash_value = user.password
    if check_password_hash(hash_value, password):
        session["username"] = username
        session["user_id"] = user.id
        session["is_admin"] = user.is_admin
        session["csrf_token"] = token_hex(16)
        return True
    return False


def logout():
    del session["username"]
    del session["is_admin"]
    del session["user_id"]
