# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel
# 2021-12-10

from os import urandom
from flask import Flask, request, redirect, render_template, session
import urllib.request
import json
import random
import requests #Using requests because we get a 403 error otherwise



app = Flask(__name__)
app.secret_key = urandom(32)


@app.route("/", methods=['GET', 'POST'])
def disp_home():
    return render_template('home.html')


@app.route("/furrbook", methods=['GET', 'POST'])
def profile_generate():
    jokes = urllib.request.urlopen('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist')
    catFacts = urllib.request.urlopen('https://cat-fact.herokuapp.com/facts')
    catList = json.loads(catFacts.read())
    jokesDict = json.loads(jokes.read())
    randomIndex = random.randrange(0,len(catList)-1)
    duckPic = requests.get('https://random-d.uk/api/v2/random', headers={'User-Agent': 'Mozilla/5.0'})
    duckDict = duckPic.json()
    print(duckDict['url'])
    fullJoke = ""
    if "joke" in jokesDict:
        fullJoke = jokesDict["joke"]
    else:
        fullJoke = jokesDict["setup"] + "<br>" + jokesDict["delivery"]
    return render_template('furrbook.html', joke = fullJoke, duckPic = duckDict['url'], catFact = catList[randomIndex]['text'])

# def home():
#     return "hello"

app.debug = True
app.run()
