# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel
import json
from os import curdir
import random
import requests
import urllib.request
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

from requests.api import get
from auth import *

team_flag = 'https://raw.githubusercontent.com/naronesty/P01/main/flag.jpg'
create_db()
# db = sqlite3.connect("hamster.db", check_same_thread=False)
# c = db.cursor()

# global pid, uName
global uName
# pid = 0
uName = ""

# api keys
f = open("keys\\key_nasa.txt", "r")
key_nasa = f.readline()
f.close()
f = open("keys\\key_openweathermap.txt", "r")
key_weather = f.readline()
f.close()
f = open("keys\\key_unsplash.txt", "r")
key_unsplash = f.readline()
f.close()

# Images API
def duckPic():
    ''' Returns url of a random duck image from random-d.uk '''
    try:
        duckPic = requests.get('https://random-d.uk/api/v2/random', headers={'User-Agent': 'Mozilla/5.0'})
        duckDict = duckPic.json()
        return duckDict['url']
    except:
        return team_flag


def dogPic():
    ''' Returns url of a random dog image from api.thedogapi.com '''
    try:
        request = urllib.request.urlopen("https://api.thedogapi.com/v1/images/search")
        dogDict = json.loads(request.read())
        return dogDict[0]["url"]
    except:
        return team_flag


def NasaImg():
    ''' Returns url of APOD of a random date from api.nasa.gov '''
    try:
        year = 2017 + random.randint(0, 3)
        month = random.randint(1, 12)
        if month == 2:
            day = random.randint(1, 29)
        elif month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 31)  # rand day from months with 31 days
        year = str(year)
        month = str(month).zfill(2)
        day = str(day).zfill(2)  # all days and months are 2 digits, adds zero if needed
        nasa = urllib.request.urlopen(
            'https://api.nasa.gov/planetary/apod?api_key=' + key_nasa + '&date=' + year + "-" + month + "-" + day)
        nasaDict = json.loads(nasa.read())  # json.loads converts the string from nasa.read() into a dictionary
        return nasaDict["url"]
    except:
        return team_flag


def unsplash(genre):
    '''
    Takes in genre and searches for results from unsplash
    Returns url of a random image from api.unsplash.com
    '''
    try:
        if genre == "Space":
            genre = "astronaut"
        unsplash = urllib.request.urlopen(
            "https://api.unsplash.com/search/photos?query=" + genre + "&client_id=" + key_unsplash)
        usDict = json.loads(unsplash.read())
        results = usDict["results"]
        randInd = random.randrange(0, len(results))
        return usDict["results"][randInd]["urls"]["raw"]  # results > rand list item > urls > raw
    except:
        return team_flag


def getMeme(chosenGenre):
    ''' Takes in genre and returns the url of a random image from corresponding subreddit '''
    try:
        subreddit = "wholesomememes"
        if chosenGenre == "Space":
            subreddit = "AstronomyMemes"
        elif chosenGenre == "Duck":
            subreddit = "DuckMemes"
        elif chosenGenre == "Dog":
            subreddit = "dogmemes"
        memeReq = urllib.request.urlopen("https://meme-api.herokuapp.com/gimme/" + subreddit + "/1")
        memeDict = json.loads(memeReq.read())["memes"][0]
        if (memeDict["nsfw"]):  # if nsfw meme, try again
            return getMeme(chosenGenre)
        return memeDict["url"]
    except:
        return team_flag


# Facts API
def catFact():
    '''
    Returns random cat fact from cat-fact.herokuapp.com

    If fail, returns "Cats are pretty cool"
    '''
    try:
        catFacts = urllib.request.urlopen('https://cat-fact.herokuapp.com/facts')
        catList = json.loads(catFacts.read())
        randomIndex = random.randrange(0, len(catList) - 1)
        return catList[randomIndex]['text']
    except:
        return "Cats are pretty cool"


def jokeFact():
    '''
    Returns random joke from v2.jokeapi.dev; excludes nsfw, racist, sexist, explicit jokes

    If fail, returns chicken joke
    '''
    try:
        jokes = urllib.request.urlopen('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist,explicit')
        jokesDict = json.loads(jokes.read())
        fullJoke = ""
        if "joke" in jokesDict:
            fullJoke = jokesDict["joke"]
        else:
            fullJoke = jokesDict["setup"] + "<br>" + jokesDict["delivery"]
        return fullJoke
    except:
        return "Why did the chicken cross the road?<br>To get to the other side..."


def factFact():
    '''
    Returns random fact from asli-fun-fact-api.herokuapp.com

    If fail, returns mcdonalds fact
    '''
    try:
        jokes = urllib.request.urlopen('https://asli-fun-fact-api.herokuapp.com/')
        jokesDict = json.loads(jokes.read())
        if (jokesDict["data"]["fact"] == "<img src=\"https://asli-fun-fact-api.herokuapp.com/fun-facts-api.jpg\" width='300px' alt='fun facts api'\/>"):
            return "Since the inception of the Happy Meal, McDonald's has become the largest distributor of toys in the world"
        return jokesDict["data"]["fact"]
    except:
        return "Since the inception of the Happy Meal, McDonald's has become the largest distributor of toys in the world"


def weatherFact():
    '''
    Returns dictionary with current weather in a random city

    If fail, returns dictionary with fake weather
    '''
    try:
        weatherTypes = ['London', 'New%20York', 'Tokyo', 'Los%20Angeles', 'Hong%20Kong', 'Mumbai', 'Meijing',
                        'Mexico%20City', 'Kinshasa', 'Lagos', 'Dhaka', 'Singapore']
        randomIndex2 = random.randrange(0, len(weatherTypes))
        weatherType = weatherTypes[randomIndex2]
        weather = urllib.request.urlopen(
            f"https://api.openweathermap.org/data/2.5/weather?q={weatherType}&appid=" + key_weather)
        weatherDict = json.loads(weather.read())['weather'][0]
        weatherDict["city"] = weatherTypes[randomIndex2]
        return weatherDict
    except:
        return {"id": -1,
                "main": "Cloudy",
                "description": "with a chance of meatballs",
                "icon": "000",
                "city": "Swallow Falls"}


# Other APIs
def randomWordList(type, numWords):
    '''
    Takes in word type (ie noun) and number of words needed

    Returns a list of random word(s) from random-word-form.herokuapp.com
    '''
    try:
        request = urllib.request.urlopen(f"https://random-word-form.herokuapp.com/random/{type}?count={numWords}")
        wordList = json.loads(request.read())
        return wordList
    except:
        words = []
        for i in range(0, numWords):
            words.append('<' + type + '>')
        return words


def choosePic(chosenGenre):
    if chosenGenre == "Space":
        return NasaImg()
    elif chosenGenre == "Duck":
        return duckPic()
    elif chosenGenre == "Dog":
        return dogPic()
    else:
        return unsplash(chosenGenre)  # to be replaced with more apis

def tweet(chosenGenre):
    if chosenGenre == "Space":
        return "https://twitter.com/NASA"
    elif chosenGenre == "Duck":
        return "https://twitter.com/theoregonduck"
    elif chosenGenre == "Dog":
        return "https://twitter.com/dog_rates"
    elif chosenGenre == "Emoji":
        return "https://twitter.com/Emojipedia "
    else:
        return "https://twitter.com/twitterdev"


def chooseWeather():
    weatherInfo = weatherFact()
    city = ""
    for i in range(0, len(weatherInfo['city'])):  # skip any %20's
        currChar = weatherInfo['city'][i]
        if currChar == '%':
            city += ' '
        elif not (currChar == '2' or currChar == '0'):
            city += currChar
    return "I love living in " + city + ". Right now the weather is " + weatherInfo['main'] + " (" + weatherInfo[
        'description'] + ")"



# Saving profile
def saveProfile():
    global uName
    currentuser="l"
    try:
        if 'username' in session:
            user = session['username']
            db = sqlite3.connect(DB_FILE)
            c = db.cursor()

            list = []
            c.execute('SELECT COUNT(pid) FROM profiles')
            rows = c.fetchall()  # fetches results of query
            for row in rows:
                list.append(row[0])
            pid = list[0]

            names = []
            query = 'INSERT INTO profiles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
            # c.execute(query, [pid, user['name'], uName, user['Filename'], user['pfp'], user['randomImg'], user['adjective'],
            #                   user['animal'], user['joke'], user['cat'], user['weather'],
            #                   user['meme1'], user['meme2'], user['age'], user['location'], user['genre'], user['date'],
            #                   user['year']])
            c.execute(query, [pid, session['profile']['name'], session['username'], session['profile']['Filename'], session['profile']['pfp'],
                             session['profile']['randomImg'], session['profile']['adjective'], session['profile']['animal'], session['profile']['joke'],
                             session['profile']['cat'], session['profile']['weather'], session['profile']['meme1'], session['profile']['meme2'],
                             session['profile']['age'], session['profile']['location'], session['profile']['genre'], session['profile']['date'],
                             session['profile']['year'], session['profile']['factList'], session['profile']['jokeList']])
            db.commit()
    except:
        return render_template('home.html')

# Rendering
def renderProfile(Filename, chosenGenre, factContent):
    global uName
    '''
    Takes in name of html template, genre, and amount of facts

    Generates the profile page using the preferances above and different APIs
    '''

    # Random Username
    adjective = randomWordList('adjective', 1)[0].capitalize()
    while "-" in adjective:
        adjective = randomWordList('adjective', 1)[0].capitalize()
    animal = randomWordList('animal', 1)[0].capitalize()
    name = adjective + " " + animal

    # Random Banner/Theme Picture
    randomImg = choosePic(chosenGenre)
    randomTweet = tweet(chosenGenre)
    # Weather of Random City
    weatherFull = chooseWeather()

    otherGenres = ["Space", "Emoji", "Duck", "Dog"]
    otherGenres.remove(chosenGenre)

    cat = catFact()
    pfp = unsplash(chosenGenre)

    # joke = jokeFact()
    factContent = int(factContent)
    weight1 = 10 - factContent
    randJoke = random.choices([jokeFact(), jokeFact(), catFact(), weatherFull], weights=[weight1, weight1, factContent, factContent], k=1)
    joke = randJoke[0]

    post1 = getMeme(chosenGenre)
    post2 = getMeme(chosenGenre)
    randAge = random.randint(18, 50)
    randLoc = random.randint(1, 12450)  # circumference/2
    genre = chosenGenre
    other_genres = otherGenres
    randDate = random.randint(1, 30)
    randYear = random.randint(1977, 2022)

    factContent = int(factContent)
    factsList = []
    jokesList = []
    for i in range(0, factContent):
        factsList.append(factFact())
    for i in range(0, 10 - factContent):
        jokesList.append(jokeFact())

    accName = ""
    # Saving Current Profile to user's session (temporary)
    if 'username' in session:
        accName = session['username']
        # uName = str(session['username'])
        # session['username'] = {}
        # user = session['username']
        # user['name'] = name
        # user['Filename'] = Filename
        # user['pfp'] = pfp
        # user['randomImg'] = randomImg
        # user['adjective'] = adjective
        # user['animal'] = animal
        # user['joke'] = joke
        # user['cat'] = cat
        # user['weather'] = weatherFull
        #
        # user['meme1'] = post1
        # user['meme2'] = post2
        # user['age'] = randAge
        # user['location'] = randLoc
        # user['genre'] = genre
        # # user['other_genres'] = other_genres
        # user['date'] = randDate
        # user['year'] = randYear

        profile = {'name': name, 'Filename': Filename, 'pfp': pfp, 'randomImg': randomImg, 'adjective': adjective, 'animal': animal,
                   'joke': joke, 'cat': cat, 'weather': weatherFull, 'meme1': post1, 'meme2': post2, 'age': randAge, 'location': randLoc,
                   'genre': genre, 'date': randDate, 'year': randYear, 'factList' : '|'.join(factsList), 'jokeList' : '|'.join(jokesList)}
        session['profile'] = profile

    return render_template(Filename,
                           joke=joke,
                           catFact=cat,
                           weatherFact=weatherFull,
                           themePic=randomImg,
                           pfp=pfp,
                           adjective=adjective,
                           animal=animal,
                           tweet = randomTweet,
                           post1=post1, post2=post2,
                           randAge=randAge,
                           randLoc=randLoc,  # circumference/2
                           genre=genre,
                           other_genres=other_genres,
                           randDate=randDate,
                           randYear=randYear,
                           facts=factsList,
                           jokes=jokesList,
                           accName=accName)

    # doesnt check if post1 and post2 are the same


def render_from_db(id):
    ''' Generates a profile from info saved in database '''
    chosenGenre = getValue('genre', id)
    otherGenres = ["Space", "Emoji", "Duck", "Dog"]
    otherGenres.remove(chosenGenre)

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    # print(id)
    template = str(getValue('template', id))
    return render_template(
        template,
        joke=getValue('joke', id),
        catFact=getValue('catFact', id),
        weatherFact=getValue('weatherFact', id),
        themePic=getValue('banner', id),
        pfp=getValue('pfp', id),
        adjective=getValue('adjective', id),
        animal=getValue('animal', id),
        post1=getValue('meme1', id), post2=getValue('meme2', id),
        randAge=getValue('age', id),
        randLoc=getValue('location', id),
        genre=chosenGenre,
        other_genres=otherGenres,
        randDate=getValue('date', id),
        randYear=getValue('year', id),
        input='saved',
        facts=getValue('factList', id).split('|'),
        jokes=getValue('jokeList', id).split('|')
    )

#for reference
# (pid INTEGER, name TEXT, username TEXT, template TEXT, pfp TEXT, banner TEXT, adjective TEXT, animal TEXT, joke TEXT, catFact TEXT, weatherFact TEXT);
# banner is sometimes a yt embed and doesnt display properly(displays black image)


def getValue(value, id):
    # print(id)
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    ''' Gets a certain value from db table with the given id '''
    list = []
    query = 'SELECT ' + value + ' FROM profiles WHERE pid = ' + str(id).replace('\'', '').replace('[', '').replace(']', '')
    print(query)
    c.execute(query)
    rows = c.fetchall()  # fetches results of query
    for row in rows:
        list.append(row[0])

    # print(list[0])
    return list[0]


def delete_profile(profile_name):
    ''' Delete saved profile '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DELETE FROM profiles WHERE name = \'" + str(profile_name) + "\'")
    db.commit()

    return True
