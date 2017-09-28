from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def view_origins():
    r = requests.get('http://ping-store.herokuapp.com/origins')
    json = r.json()
    origins = { o['origin']:o['links'][0]['href'] for o in json}
    # założenie o jednym linku!
    # dlaczego potrzebne [] zamiast .?
    return render_template('index.html', origins=origins )
