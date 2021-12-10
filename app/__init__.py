# Hamsters of Destiny -- Annabel Zhang, Noakai Aronesty, Hebe Huang, Justin Zou
# SoftDev
# P01 -- The Hamster Wheel
from os import urandom
from flask import Flask, request, redirect, render_template, session
import urllib.request
import json
import random

app = Flask(__name__)
app.secret_key = urandom(32)

from app import main

app.debug = True
app.run()
