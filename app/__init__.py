# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel
# 2021-12-10

from os import urandom
from flask import Flask, request, redirect, render_template, session
import urllib.request
import json
import random


app = Flask(__name__)
app.secret_key = urandom(32)


@app.route("/")
def profile_generate():
    jokes = urllib.request.urlopen('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist')
    catFacts = urllib.request.urlopen('https://cat-fact.herokuapp.com/facts')
    catList = json.loads(catFacts.read())
    jokesDict = json.loads(jokes.read())
    randomIndex = random.randrange(0,len(catList))
    # duckPic = urllib.request.urlopen('https://random-d.uk/api/v2/randomimg')
    if "joke" in jokesDict:
        return jokesDict["joke"]
    
    return jokesDict["setup"] + "<br>" + jokesDict["delivery"] + "<br>" + catList[randomIndex]['text'] 
# def home():
#     return "hello"

app.debug = True
app.run()
