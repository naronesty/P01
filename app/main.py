# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel


from os import urandom
from flask import Flask, request, redirect, render_template, session
import urllib.request
import json
import random
from app import app

# def home():
#     return "hello"

@app.route("/")
def profile_generate():
    jokes = urllib.request.urlopen('https://v2.jokeapi.dev/joke/Christmas')
    d = json.loads(jokes.read())