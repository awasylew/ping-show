from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def lits_origins():
    r = requests.get('http://ping-store.herokuapp.com/origins')
    # json = r.json()
    origins = { o['origin']:o['links'][0]['href'] for o in r.json()}
    # założenie o jednym linku!
    # dlaczego potrzebne [] zamiast .?
    return render_template('index.html', origins=origins )

@app.route('/origin')
def show_origin():
    link = request.args.get('link')
    r = requests.get(link)
#    json = r.json()
#    return str(json), 200
    print(r.json())
    targets = { target['target']:target for target in r.json()}
    return render_template('show_origin.html', targets=targets)
