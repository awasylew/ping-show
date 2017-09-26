from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def view_origins():
    r = requests.get('http://ping-store.herokuapp.com/origins')
    return r.text
