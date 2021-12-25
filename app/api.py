# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel
import json
from os import curdir
import random
import requests
import urllib.request
from flask import Flask, render_template, request, session, redirect, url_for

team_flag = 'https://raw.githubusercontent.com/naronesty/P01/main/flag.jpg'

#Images API
def duckPic():
    try:
        duckPic = requests.get('https://random-d.uk/api/v2/random', headers={'User-Agent': 'Mozilla/5.0'})
        duckDict = duckPic.json()
        return duckDict['url']
    except:
        return team_flag


def dogPic():
    try:
        request = urllib.request.urlopen("https://api.thedogapi.com/v1/images/search")
        dogDict= json.loads(request.read())
        return dogDict[0]["url"]
    except:
        return team_flag


def NasaImg():
    try:
        year = 2017 + random.randint(0, 3)
        month = random.randint(1, 12)
        if month == 2:
            day = random.randint(1, 29)
        elif month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 31) # rand day from months with 31 days
        year = str(year)
        month = str(month).zfill(2)
        day = str(day).zfill(2) # all days and months are 2 digits, adds zero if needed
        nasa = urllib.request.urlopen('https://api.nasa.gov/planetary/apod?api_key=7FDdoAzbN5DoWCsTmAqZz3NIeHSGgaDd6nxUTvWJ&date=' + year + "-" + month + "-" + day)
        nasaDict = json.loads(nasa.read())  # json.loads converts the string from nasa.read() into a dictionary
        return nasaDict["url"]
    except:
        return team_flag


def unsplash(genre):
    try:
        if genre == "Space":
            genre = "astronaut"
        unsplash = urllib.request.urlopen("https://api.unsplash.com/search/photos?query=" + genre + "&client_id=BaCufkOBYk3YdZorWqjhxi0eeaXXbfzHVKbDKBNX9vo")
        usDict = json.loads(unsplash.read())
        results = usDict["results"]
        randInd = random.randrange(0, len(results))
        return usDict["results"][randInd]["urls"]["raw"]  # results > rand list item > urls > raw
    except:
        return team_flag


def getMeme(chosenGenre):
    try:
        subreddit = "wholesomememes"
        if chosenGenre == "Space":
            subreddit = "space_memes"
        elif chosenGenre == "Duck":
            subreddit = "DuckMemes"
        memeReq = urllib.request.urlopen("https://meme-api.herokuapp.com/gimme/" + subreddit + "/1")
        memeDict = json.loads(memeReq.read())["memes"][0]
        if(memeDict["nsfw"]):  # if nsfw meme, try again
            return getMeme(chosenGenre)
        return memeDict["url"]
    except:
        return team_flag


#Facts API
def catFact():
    try:
        catFacts = urllib.request.urlopen('https://cat-fact.herokuapp.com/facts')
        catList = json.loads(catFacts.read())
        randomIndex = random.randrange(0, len(catList) - 1)
        return catList[randomIndex]['text']
    except:
        return "Cats are pretty cool"


def jokeFact():
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


def weatherFact():
    try:
        weatherTypes = ['London', 'New%20York', 'Tokyo', 'Los%20Angeles', 'Hong%20Kong', 'Mumbai', 'Meijing', 'Mexico%20City', 'Kinshasa', 'Lagos', 'Dhaka', 'Singapore']
        randomIndex2 = random.randrange(0, len(weatherTypes))
        weatherType = weatherTypes[randomIndex2]
        weather = urllib.request.urlopen(
            f"https://api.openweathermap.org/data/2.5/weather?q={weatherType}&appid=5c727cbb8c6ef9847ebc43a14d501562")
        weatherDict = json.loads(weather.read())['weather'][0]
        weatherDict["city"] = weatherTypes[randomIndex2]
        return weatherDict
    except:
        return {"id": -1,
         "main": "Cloudy",
         "description": "with a chance of meatballs",
         "icon": "000",
         "city": "Swallow Falls"}


#Other APIs
def randomWordList(type, numWords):
    try:
        request = urllib.request.urlopen(f"https://random-word-form.herokuapp.com/random/{type}?count={numWords}")
        wordList = json.loads(request.read())
        return wordList
    except:
        words = []
        for i in range(0, numWords):
            words.append('<' + type + '>')
        return words


#Rendering
def renderProfile(Filename, chosenGenre, factContent):
    adjective=randomWordList('adjective', 1)[0].capitalize()
    while "-" in adjective:
        adjective=randomWordList('adjective', 1)[0].capitalize()
    if chosenGenre == "Space":
        randomImg = NasaImg()
    elif chosenGenre == "Duck":
        randomImg = duckPic()
    elif chosenGenre == "Dog":
        randomImg = dogPic()
    else:
        randomImg = unsplash(chosenGenre) #to be replaced with more apis
    weatherInfo = weatherFact()
    city = ""
    for i in range(0, len(weatherInfo['city'])): # skip any %20's
        currChar = weatherInfo['city'][i]
        if currChar == '%':
            city += ' '
        elif not (currChar == '2' or currChar == '0'):
            city += currChar
    weatherFull = "I love living in " + city + ". Right now the weather is " + weatherInfo['main'] + " (" + weatherInfo['description'] + ")"
    otherGenres = ["Space", "Emoji", "Duck", "Dog"]
    otherGenres.remove(chosenGenre)
    
    return render_template(Filename,
    joke=jokeFact(),
    #random.choices([jokeFact(), jokeFact(), catFact(), weatherFull], weights=[10-factContent, 10-factContent, factContent, factContent], k=1),
                           catFact=catFact(),
                           weatherFact=weatherFull,
                           themePic=randomImg,
                           pfp=unsplash(chosenGenre),
                           adjective=adjective,
                           animal=randomWordList('animal', 1)[0].capitalize(),
                           post1 = getMeme(chosenGenre), post2 = getMeme(chosenGenre),
                           randAge = random.randint(18, 50),
                           randLoc = random.randint(1, 12450), # circumference/2
                           genre = chosenGenre,
                           other_genres = otherGenres)
                           #doesnt check if post1 and post2 are the same
