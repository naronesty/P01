# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel
from os import urandom
from flask import Flask, request, redirect, render_template, session
import urllib.request
import json
import random

app = Flask(__name__)

from app import main

if __name__ == "__main__":
    app.debug = True
    app.secret_key = urandom(32)
    app.run()
