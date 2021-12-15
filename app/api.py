# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel
import json
import random
import requests
import urllib.request

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
    nasa = urllib.request.urlopen(
        'https://api.nasa.gov/planetary/apod?api_key=7FDdoAzbN5DoWCsTmAqZz3NIeHSGgaDd6nxUTvWJ')
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
    unsplash = urllib.request.urlopen(
        "https://api.unsplash.com/search/photos?page=1&query=" + genre + "&client_id=BaCufkOBYk3YdZorWqjhxi0eeaXXbfzHVKbDKBNX9vo")
    usDict = json.loads(unsplash.read())
    results = usDict["results"]
    randInd = random.randrange(0, len(results))
    print("randint  " + str(randInd))
    return usDict["results"][randInd]["urls"]["raw"]  # results > first list item > urls > raw


def randomWord(numWords):
    return