# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel
# 2021-12-10

from os import urandom
from flask import Flask, render_template, request, session, redirect, url_for
import urllib.request
import json
import random
import requests  # Using requests because we get a 403 err  or otherwise
from auth import *

app = Flask(__name__)
app.secret_key = urandom(32)

create_db()

@app.route("/", methods=['GET', 'POST'])
def disp_home():
    return render_template('home.html')


@app.route("/generate", methods=['GET', 'POST'])
def profile_generate():
    if request.method == 'POST':  # determine which template to render
        chosenTemp = request.form['templateMenu']
        chosenGenre = request.form['genreMenu']
        print(chosenGenre)  # testing to see if we can access the genre user picked
        if chosenTemp == "RandomChosen":
            dice = random.randint(0,2)
            print(dice)
            if dice == 0:
                chosenTemp = "FurrbookChosen"
            elif dice == 1:
                chosenTemp = "DestinderChosen"
            elif dice == 2:
                chosenTemp = "HamstwitterChosen"
            print(chosenTemp)
        if chosenTemp == "FurrbookChosen":
            return render_template('furrbook.html', greet = helloSalut(), joke=jokeFact(), duckPic=duckPic(),
                                    catFact=catFact(),
                                    weatherFact=weatherFact()['main'] + " " + weatherFact()['description'],
                                    NasaPic = NasaImg(),
                                    themePic = unsplash(chosenGenre))
        elif chosenTemp == "DestinderChosen":
            return render_template('destinder.html', greet = helloSalut(), joke=jokeFact(), duckPic=duckPic(),
                                    catFact=catFact(),
                                    weatherFact=weatherFact()['main'] + " " + weatherFact()['description'],
                                    NasaPic = NasaImg(),
                                    themePic = unsplash(chosenGenre))
        elif chosenTemp == "HamstwitterChosen":
            return render_template('hamstwitter.html', greet = helloSalut(), joke=jokeFact(), duckPic=duckPic(),
                                    catFact=catFact(),
                                    weatherFact = weatherFact()['main'] + " " + weatherFact()['description'],
                                    NasaPic = NasaImg(),
                                    themePic = unsplash(chosenGenre))
#should make helper function w/ rendering each template
        # elif chosenTemp == "RandomChosen":
        #     dice = random.randint(0,2)
        #     print(dice)
        #     if dice == 0:
        #         return render_template('furrbook.html', joke=jokeFact(), duckPic=duckPic(),
        #                     catFact=catFact(),
        #                     weatherFact = weatherFact()['main'] + " " + weatherFact()['description'])
        #     if dice == 1:
        #         return render_template('destinder.html', joke=jokeFact(), duckPic=duckPic(),
        #                      catFact=catFact(),
        #                      weatherFact = weatherFact()['main'] + " " + weatherFact()['description'])
        #     if dice == 2:
        #         return render_template('hamstwitter.html', joke=jokeFact(), duckPic=duckPic(),
        #                      catFact=catFact(),
        #                      weatherFact = weatherFact()['main'] + " " + weatherFact()['description'])
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
    nasa = urllib.request.urlopen('https://api.nasa.gov/planetary/apod?api_key=7FDdoAzbN5DoWCsTmAqZz3NIeHSGgaDd6nxUTvWJ')
    nasaDict = json.loads(nasa.read())  # json.loads converts the string from nasa.read() into a dictionary
    return nasaDict["url"]


def weatherFact():
    weatherTypes = ['London', 'New%20York', 'Tokyo', 'Los%20Angeles', 'hong%20kong']
    randomIndex2 = random.randrange(0, len(weatherTypes))
    weatherType = weatherTypes[randomIndex2]
    weather = urllib.request.urlopen(
        f"https://api.openweathermap.org/data/2.5/weather?q={weatherType}&appid=5c727cbb8c6ef9847ebc43a14d501562")
    weatherDict = json.loads(weather.read())
    return weatherDict['weather'][0]

def helloSalut():
    langs = ["en", "es", "fr", "ja", "zh"]
    # ar, az, be, bg, bn, bs, cs, da, de, dz, el, en, en-gb, en-us, es, et, fa, fi, fil, fr, he, hi, hr, hu, hy, id, is, it, ja, ka, kk, km, ko, lb, lo, lt, lv, mk, mn, ms, my, ne, no, pl, pt, ro, ru, sk, sl, sq, sr, sv, sw, th, tk, uk, vi, zh
    lang = langs[random.randrange(len(langs))]
    helloSalut = urllib.request.urlopen("https://fourtonfish.com/hellosalut/?lang=" + lang)
    hsDict = json.loads(helloSalut.read())
    return hsDict["hello"]

def unsplash(genre):
    unsplash = urllib.request.urlopen("https://api.unsplash.com/search/photos?page=1&query=" + genre + "&client_id=BaCufkOBYk3YdZorWqjhxi0eeaXXbfzHVKbDKBNX9vo")
    usDict = json.loads(unsplash.read())
    results = usDict["results"]
    randInd = random.randrange(0, len(results))
    print("randint  " + str(randInd))
    return usDict["results"][randInd]["urls"]["raw"] # results > first list item > urls > raw

# authetication of login
@app.route("/auth", methods=['GET', 'POST'])
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
        return redirect(url_for('disp_home'))

    auth_state = auth_user(username, password)
    if auth_state == True:
        session['username'] = username
        return redirect(url_for('disp_home'))
    elif auth_state == "bad_pass":
        return render_template('login.html', input="bad_pass")
    elif auth_state == "bad_user":
        return render_template('login.html', input="bad_user")

@app.route("/register")
def register():
        ''' Displays register page '''

        return render_template('register.html')

@app.route("/login")
def login():
        ''' Displays login page '''

        return render_template('login.html')

@app.route("/rAuth", methods=['GET', 'POST'])
def rAuthenticate():
        ''' Authentication of username and passwords given in register page from user '''

        method = request.method
        username = request.form.get('username')
        password0 = request.form.get('password0')
        password1 = request.form.get('password1')

        if method == 'GET':
            return redirect(url_for('register'))

        if method == 'POST':
            # error when no username is inputted
            if len(username) == 0:
                return render_template('register.html', given="username")
            # error when no password is inputted
            elif len(password0) == 0:
                return render_template('register.html', given="password")
            elif len(password0) < 8:
                return render_template('register.html', given="password greater than 8 characters")
            # a username and password is inputted
            # a username and password is inputted
            else:
                # if the 2 passwords given don't match, will display error saying so
                if password0 != password1:
                    return render_template('register.html', mismatch=True)
                else:
                    # creates user account b/c no fails
                    if create_user(username, password0):
                        return render_template('login.html', input='success')
                    # does not create account because create_user failed (username is taken)
                    else:
                        return render_template('register.html', taken=True)

@app.route("/logout")
def logout():
    ''' Logout user by deleting user from session dict. Redirects to loginpage '''

    # Delete user. This try... except... block prevent an error from ocurring when the logout page is accessed from the login page
    try:
        session.pop('username')
    except KeyError:
        return redirect(url_for('disp_home'))
    # Redirect to login page
    return redirect(url_for('disp_home'))

# def home():
#     return "hello"

app.debug = True
app.run()
