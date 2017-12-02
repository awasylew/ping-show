from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

base = os.getenv('STORE_URL')

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
    r = requests.get(base+'/targets', {'origin':origin})
    return render_template('show_origin.html', base=base, origin=origin, targets=r.json())

@app.route('/list_minutes/<origin>/<target>')
def list_minutes(origin, target):
    r = requests.get(base+'/minutes', {'origin':origin, 'target':target})
    return render_template('list_minutes.html', origin=origin, target=target, minutes=r.json())

def time_as_date(time):
    return time[0:4]+'-'+time[4:6]+'-'+time[6:8]

def time_as_date_hour(time):
    return time[0:4]+'-'+time[4:6]+'-'+time[6:8]+' '+time[8:10]+':00'

@app.route('/list_hours/<origin>/<target>')
def list_hours(origin, target):
    r = requests.get(base+'/hours', {'origin':origin, 'target':target})
    data = { time_as_date_hour(hour['hour']): \
        {'hour':hour['hour'], 'count':hour['count'], \
            'min_rtt':hour['min_rtt'], 'max_rtt':hour['max_rtt'], \
            'avg_rtt':'%.2f' % hour['avg_rtt'], \
            'success_rate':round(100.0*hour['count_success']/hour['count'])} \
        for hour in r.json()}
    return render_template('list_hours.html', origin=origin, target=target, \
        hours=r.json(), data=data)

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
