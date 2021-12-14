# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel
# 2021-12-10

from os import urandom
from flask import Flask, request, redirect, render_template, session
import urllib.request
import json
import random
import requests  # Using requests because we get a 403 error otherwise

app = Flask(__name__)
app.secret_key = urandom(32)


@app.route("/", methods=['GET', 'POST'])
def disp_home():
    return render_template('home.html')


@app.route("/generate", methods=['GET', 'POST'])
def profile_generate():
    if request.method == 'POST': # determine which template to render
        chosenTemp = request.form['templateMenu']
        print(request.form['genreMenu']) # testing to see if we can access the genre user picked
        if chosenTemp == "FurrbookChosen":
            return render_template('furrbook.html', joke=jokeFact(), duckPic=duckPic(),
                           catFact=catFact(),
                           weatherFact = weatherFact()['main'] + " " + weatherFact()['description'])
        elif chosenTemp == "DestinderChosen":
            return render_template('destinder.html', joke=jokeFact(), duckPic=duckPic(),
                           catFact=catFact(),
                           weatherFact = weatherFact()['main'] + " " + weatherFact()['description'])
        elif chosenTemp == "HamstwitterChosen":
            return render_template('hamstwitter.html', joke=jokeFact(), duckPic=duckPic(),
                           catFact=catFact(),
                           weatherFact = weatherFact()['main'] + " " + weatherFact()['description'])
    return render_template('home.html') # user did not select a template or something went wrong

def catFact():
    catFacts = urllib.request.urlopen('https://cat-fact.herokuapp.com/facts')
    catList = json.loads(catFacts.read())
    randomIndex = random.randrange(0, len(catList) - 1)
    return catList[randomIndex]['text']


def duckPic():
    duckPic = requests.get('https://random-d.uk/api/v2/random', headers={'User-Agent': 'Mozilla/5.0'})
    duckDict = duckPic.json()
    return duckDict['url']

def jokeFact():
    jokes = urllib.request.urlopen('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist')
    jokesDict = json.loads(jokes.read())
    fullJoke = ""
    if "joke" in jokesDict:
        fullJoke = jokesDict["joke"]
    else:
        fullJoke = jokesDict["setup"] + "<br>" + jokesDict["delivery"]
    return fullJoke

def NasaImg():
    nasa = urllib.request.urlopen('https://api.nasa.gov/planetary/apod?api_key=' + api_key)
    nasaDict = json.loads(nasa.read()) #json.loads converts the string from nasa.read() into a dictionary
    return nasaDict["url"]

def weatherFact():
    weatherTypes = ['London','New%20York','Tokyo','Los%20Angeles','hong%20kong']
    randomIndex2 = random.randrange(0,len(weatherTypes))
    weatherType = weatherTypes[randomIndex2]
    weather = urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?q={weatherType}&appid=5c727cbb8c6ef9847ebc43a14d501562")
    weatherDict = json.loads(weather.read())
    return weatherDict['weather'][0]

# authetication of login
@app.route("/auth", methods=['GET','POST'])
def authenticate():
    ''' Checks whether method is get, post. If get method, then redirect to
       loginpage. If post, then authenticate the username and password, rendering
       the error page if incorrect and the response.html if correct username/pass. '''

    # Variables
    method = request.method
    username = request.form.get('username')
    password = request.form.get('password')

    # Get vs Post
    if method == 'GET':
        return redirect(url_for('index'))

    auth_state = auth_user(username, password)
    if auth_state == True:
        session['username'] = username
        return redirect(url_for('index'))
    elif auth_state == "bad_pass":
        return render_template('login.html', input="bad_pass")
    elif auth_state == "bad_user":
        return render_template('login.html', input="bad_user")

# def home():
#     return "hello"



app.debug = True
app.run()
