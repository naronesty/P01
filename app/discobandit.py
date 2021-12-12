# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel
import sqlite3


db = sqlite3.connect("hamster.db", check_same_thread=False)
c = db.cursor()

# creates users and profiles tables
# pid is profile id
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, pid TEXT)")
# picture is profile pic; banner is profile banner
c.execute("CREATE TABLE IF NOT EXISTS profiles(id INTEGER, username TEXT, picture TEXT, banner TEXT, biography TEXT, hobbies TEXT);")
db.commit()