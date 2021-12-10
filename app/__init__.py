from flask import Flask, request, redirect, render_template, session
import urllib.request
import json
import random

app = Flask(__name__)


# def home():
#     return "hello"

@app.route("/")
def profile_generate():
    jokes = urllib.request.urlopen('https://v2.jokeapi.dev/joke/Christmas')
    d = json.loads(jokes.read())
    try


if __name__ == "__main__":
    app.debug = True
    app.secret_key = "It's Rewind Time"
    app.run()
