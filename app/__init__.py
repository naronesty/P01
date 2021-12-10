# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel

from os import urandom
from flask import Flask

app = Flask(__name__)
app.secret_key = urandom(32)

from app import main

if __name__ == "__main__":
    app.debug = True
    app.run()
