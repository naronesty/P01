# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel
# 2021-12-10

from os import urandom
from flask import Flask, request, redirect, render_template, session
import urllib.request
import json
import sqlite3
import random


db = sqlite3.connect("hamster.db", check_same_thread=False)
c = db.cursor()

# creates users and profiles tables
# pid is profile id
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, pid TEXT)")
# picture is profile pic; banner is profile banner
c.execute("CREATE TABLE IF NOT EXISTS profiles(id INTEGER, username TEXT, picture TEXT, banner TEXT, biography TEXT, hobbies TEXT);")
db.commit()


app = Flask(__name__)
app.secret_key = urandom(32)


@app.route("/")
def profile_generate():
    jokes = urllib.request.urlopen('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist')
    d = json.loads(jokes.read())
    if "joke" in d:
        return d["joke"]
    return d["setup"] + "<br>" + d["delivery"]

# def home():
#     return "hello"

app.debug = True
app.run()
