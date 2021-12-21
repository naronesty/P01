# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel
import json
import random
import requests
import urllib.request
from flask import Flask, render_template, request, session, redirect, url_for


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
    jokes = urllib.request.urlopen('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist,explicit')
    jokesDict = json.loads(jokes.read())
    fullJoke = ""
    if "joke" in jokesDict:
        fullJoke = jokesDict["joke"]
    else:
        fullJoke = jokesDict["setup"] + "<br>" + jokesDict["delivery"]
    return fullJoke


def NasaImg():
    nasa = urllib.request.urlopen(
            'https://api.nasa.gov/planetary/apod?api_key=7FDdoAzbN5DoWCsTmAqZz3NIeHSGgaDd6nxUTvWJ')
    nasaDict = json.loads(nasa.read())  # json.loads converts the string from nasa.read() into a dictionary
    return nasaDict["url"]


def weatherFact():
    weatherTypes = ['london', 'new%20york', 'tokyo', 'Los%20Angeles', 'hong%20kong', 'mumbai', 'beijing', 'mexico%20city', 'kinshasa', 'lagos', 'dhaka', 'singapore']
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
    if genre == "Space":
        genre = "astronaut"
    unsplash = urllib.request.urlopen("https://api.unsplash.com/search/photos?page=1&query=" + genre + "&client_id=BaCufkOBYk3YdZorWqjhxi0eeaXXbfzHVKbDKBNX9vo")
    usDict = json.loads(unsplash.read()) # currently only looks at page 1 of results
    results = usDict["results"]
    randInd = random.randrange(0, len(results))
    return usDict["results"][randInd]["urls"]["raw"]  # results > rand list item > urls > raw


def randomWordList(type, numWords):
    request = urllib.request.urlopen(f"https://random-word-form.herokuapp.com/random/{type}?count={numWords}")
    wordList = json.loads(request.read())
    return wordList

def getMeme(chosenGenre):
    subreddit = "wholesomememes"
    if chosenGenre == "Space":
        subreddit = "space_memes"
    elif chosenGenre == "Duck":
        subreddit = "DuckMemes"
    memeReq = urllib.request.urlopen("https://meme-api.herokuapp.com/gimme/" + chosenGenre + "/1")
    memeDict = json.loads(memeReq.read())["memes"][0]
    if(memeDict["nsfw"]):  # if somehow got nsfw from the wholesomemes subreddit, try again
        return getMeme()
    return memeDict["url"]

def pfpGet(chosenGenre):
    if chosenGenre == "Space":
        randomImg = NasaImg()
    elif chosenGenre == "Duck":
        randomImg = duckPic()
    else:
        randomImg = unsplash(chosenGenre) #to be replaced with more apis
    return randomImg

def renderProfile(Filename, chosenGenre):
    adjective=randomWordList('adjective', 1)[0].capitalize()
    while "-" in adjective:
        adjective=randomWordList('adjective', 1)[0].capitalize()

    if chosenGenre == "Space":
        randomImg = NasaImg()
    elif chosenGenre == "Duck":
        randomImg = duckPic()
    else:
        randomImg = unsplash(chosenGenre) #to be replaced with more apis
    return render_template(Filename, joke=jokeFact(),
                           catFact=catFact(),
                           weatherFact=weatherFact()['main'] + " " + weatherFact()['description'],
                           themePic=randomImg,
                           pfp=unsplash(chosenGenre),
                           adjective=adjective,
<<<<<<< HEAD
                           animal=randomWordList('animal', 1)[0],
                           post1 = getMeme(chosenGenre), post2 = getMeme(chosenGenre))
=======
                           animal=randomWordList('animal', 1)[0].capitalize(),
                           post1 = getMeme(), post2 = getMeme())
>>>>>>> 2f641685f8fa3413db07af59b2c235873c0e3d13
                        #    username = session['username']) #doesnt check if post1 and post2 are the same
