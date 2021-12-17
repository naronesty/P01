# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel

""" Authentication / Creation of Users """

import sqlite3

DB_FILE = "discobandit.db"

def create_db():
    ''' Creates / Connects to DB File '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (usernames TEXT, passwords TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS favorites (users TEXT, id INTEGER);")
    db.close()


def auth_user(username, password):
    ''' Validates a username + password when person logs in '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # Create List of Users
    c.execute("SELECT usernames FROM users")
    users = []
    for a_tuple in c.fetchall():
        users.append(a_tuple[0])

    if username in users:
        c.execute("SELECT passwords FROM users WHERE usernames = '" + username + "'")
        if c.fetchall()[0][0] == password:
            return True
        else:
            return "bad_pass"
    else:
        return "bad_user"


def create_user(username, password):
    ''' Adds user to database if right username and password are given when a
        person registers '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # Create List of Users
    c.execute("SELECT usernames FROM users")
    users = []
    for a_tuple in c.fetchall():
        users.append(a_tuple[0])

    # username is not taken, creates account with given username and password
    if username in users:
        return False
    else:
        c.execute("INSERT INTO users VALUES (?, ?);", (username, password))
        db.commit()
        return True

create_db()

# For testing purposes #################

# db = sqlite3.connect(DB_FILE)
# c = db.cursor()
# db.commit()
# c.execute("SELECT usernames FROM users")
# users = []
# for a_tuple in c.fetchall():
#     users.append(a_tuple[0])
# print(users)
