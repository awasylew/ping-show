from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

base = 'http://ping-store.herokuapp.com'

@app.route('/')
def list_origins():
    r = requests.get(base+'/origins')
    # origins = { o['origin']:o['links'][0]['href'] for o in r.json()}
    # założenie o jednym linku!
    # dlaczego potrzebne [] zamiast .?
    # return render_template('index.html', origins=origins )
    return render_template('index.html', origins=r.json())

@app.route('/origins/<origin>')
def show_origin(origin):
    # link = request.args.get('link')
    r = requests.get(base+'/targets', {'origin':origin})
#    targets = { target['target']:target for target in r.json()}
    return render_template('show_origin.html', base=base, origin=origin, targets=r.json())
#    return r.text

@app.route('/list_minutes/<origin>/<target>')
def list_minutes(origin, target):
    r = requests.get(base+'/minutes', {'origin':origin, 'target':target})
#    return r.text
    return render_template('list_minutes.html', origin=origin, target=target, minutes=r.json())

@app.route('/list_hours/<origin>/<target>')
def list_hours(origin, target):
    r = requests.get(base+'/hours', {'origin':origin, 'target':target})
#    return r.text
    return render_template('list_hours.html', origin=origin, target=target, hours=r.json())

@app.route('/show_minute/<origin>/<target>/<minute>')
def show_minute(origin, target, minute):
    r = requests.get(base+'/pings', {'origin':origin, 'target':target, 'time_prefix':minute})
    return r.text, 200

@app.route('/show_hour/<origin>/<target>/<hour>')
def show_hour(origin, target, hour):
    r = requests.get(base+'/pings', {'origin':origin, 'target':target, 'time_prefix':hour})
    # return r.text, 200
    return render_template('show_hour.html', origin=origin, target=target, time=hour, pings=r.json())

if __name__ == '__main__':
    port = int(os.getenv("PORT"))
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=port)
