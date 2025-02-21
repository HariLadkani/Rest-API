from flask import Flask
app = Flask(__name__)
from controller import *

@app.route("/")
def welcome():
    return "Hello World"

@app.route("/home")
def home():
    return "this is my home"