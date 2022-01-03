# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel
# 2021-12-10

from os import urandom
from flask import Flask, render_template, request, session, redirect, url_for
import urllib.request
from urllib.error import HTTPError
import json
import random
import requests  # Using requests because we get a 403 err  or otherwise
from auth import *
from api import *
import sqlite3

app = Flask(__name__)
app.secret_key = urandom(32)

create_db()
global factContent
factContent = 0

@app.route("/", methods=['GET', 'POST'])
def disp_home():
    ''' Loads the landing page '''
    return render_template('home.html')


@app.route("/generate", methods=['GET', 'POST'])
def profile_generate():
    ''' Generates a randomized profile page from preferences '''
    global genre
    if request.method == 'POST':  # determine which template to render
        chosenTemp = request.form['templateMenu']
        chosenGenre = request.form['genreMenu']
        chosenfactContent = request.form['jokesSlider']

        if chosenTemp == "RandomChosen":
            dice = random.randint(0, 2)
            print(dice)
            if dice == 0:
                chosenTemp = "FurrbookChosen"
            elif dice == 1:
                chosenTemp = "DestinderChosen"
            elif dice == 2:
                chosenTemp = "HamstwitterChosen"
            print(chosenTemp)
        if chosenGenre == "Random":
            dice = random.randint(0, 3)
            print(dice)
            if dice == 0:
                chosenGenre = "Space"
            elif dice == 1:
                chosenGenre = "Emoji"
            elif dice == 2:
                chosenGenre = "Duck"
            elif dice == 3:
                chosenGenre = "Dog"
            print(chosenGenre)
        try:
            if chosenTemp == "FurrbookChosen":
                return renderProfile("furrbook.html", chosenGenre, chosenfactContent)
            elif chosenTemp == "DestinderChosen":
                return renderProfile("destinder.html", chosenGenre, chosenfactContent)
            elif chosenTemp == "HamstwitterChosen":
                return renderProfile("hamstwitter.html", chosenGenre, chosenfactContent)
        except HTTPError:
            return render_template('home.html')
    return render_template('home.html')  # user did not select a template or something went wrong


@app.route("/save", methods=['GET', 'POST'])
def save():
    ''' Saves information on a profile in database '''

    saveProfile()

    try:
        discoverList = []
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        query = c.execute('SELECT name, template FROM profiles')

        convert = list(query) #turns tuple into list

    except:
        return render_template("home.html")

    return render_template('discover.html', list=convert)

@app.route("/discover", methods=['GET', 'POST'])
def discover():
    try:
        discoverList = []
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        query = c.execute('SELECT name, template FROM profiles')

        convert = list(query) #turns tuple into list

    except:
        return render_template("home.html")

    return render_template("discover.html", list=convert)


@app.route("/<user>", methods=['GET', 'POST'])
def view(user):
    list = []
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    query = ('SELECT pid FROM profiles WHERE name = \'' + user + '\'') #fixes issue when there's a space in name
    c.execute(query)
    rows = c.fetchall() #fetches results of query
    for row in rows:
        list.append(row[0])
    # print(list)
    return render_from_db(list[0])



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
