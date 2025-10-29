from flask import Flask
from math import *
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'