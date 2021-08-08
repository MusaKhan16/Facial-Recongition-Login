import sqlite3
from sqlite3 import Error

filepath = "Facial_Recognition/passwords.db"


def create_table():
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    cur.execute(
        """
            CREATE TABLE users(
                username text unique, password text unique)"""
    )
    con.commit()
    con.close()


def insert_to_db(user, password):
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    try:
        cur.execute(
            """INSERT INTO users(username, password) VALUES(?,?)""", (user, password)
        )
    except sqlite3.IntegrityError:
        print("Username or password exists")
    con.commit()
    con.close()


def clear_db():
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    cur.execute("""DELETE FROM users""")
    con.commit()
    con.close()


def get_password(passw):
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    found = cur.execute("""SELECT password FROM users WHERE password = (?)""", [passw])
    return [row for row in found]
