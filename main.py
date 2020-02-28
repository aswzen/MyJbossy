from flask import Flask, render_template, Response
import requests
from requests.auth import HTTPDigestAuth
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import urllib
import json

app = Flask(__name__,
            static_folder='assets',
            template_folder='templates')

app.config['APPLICATION_ROOT'] = "/monitoring"
auth = HTTPBasicAuth()
users = {
    "user1": generate_password_hash("jkt48"),
    "admin1": generate_password_hash("###3")
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False
    
@app.route('/')
@auth.login_required
def root():
    return render_template('dashboard.html')


@app.route('/dashboard')
@app.route('/dashboard/<name>')
@auth.login_required
def dashboard(name=None):
    return render_template('dashboard.html', name=name)


@app.route('/data')
def data():
    url = 'http://10.64.20.173:9990/management'
    r = requests.get(url,
                     proxies={"http": "http://10.0.144.183:8080"},
                     auth=HTTPDigestAuth('sigit', 'sigit')
                     )
    return "results "+r.text

def load(ip=None,username=None,password=None):
    url = "http://"+ip+"/management"
    r = requests.get(url,
                     proxies={"http": "http://10.0.144.183:8080"},
                     auth=HTTPDigestAuth(username, password)
                     )
    return r.text

def getState(warName=None,ip=None,username=None,password=None):
    url = "http://"+ip+"/management/deployment/"+warName+"?operation=attribute&name=enabled"
    r = requests.get(url,
                     proxies={"http": "http://10.0.144.183:8080"},
                     auth=HTTPDigestAuth(username, password)
                     )
    return r.text


@app.route('/results')
def results():
    data = {
        "total": 2,
        "records": [{
            "ip"		: "10.64.20.67",
            "port"		: "9990",
            "username"	: "sigit",
            "password"	: "sigit"
        }, {
            "ip"		: "10.64.20.128",
            "port"		: "9990",
            "username"	: "sigit",
            "password"	: "sigit"
        }, {
            "ip"		: "10.64.20.159",
            "port"		: "9990",
            "username"	: "sigit",
            "password"	: "sigit"
        }, {
            "ip"		: "10.64.20.167",
            "port"		: "9990",
            "username"	: "sigit",
            "password"	: "sigit"
        }, {
            "ip"		: "10.64.20.173",
            "port"		: "9990",
            "username"	: "sigit",
            "password"	: "sigit"
        }, {
            "ip"		: "10.64.17.12",
            "port"		: "9990",
            "username"	: "edw",
            "password"	: "password"
        }, {
            "ip"		: "10.64.17.13",
            "port"		: "9990",
            "username"	: "edw",
            "password"	: "password"
        }, {
            "ip"		: "10.64.17.20",
            "port"		: "9990",
            "username"	: "edw",
            "password"	: "password"
        }]
    }

    records = data["records"]

    for index,f in enumerate(records, start=0):
        try:
            res = load(f["ip"]+":"+f["port"],f["username"],f["password"])
            json_data = json.loads(res)
            data["records"][index]["name"] = json_data["name"]
            data["records"][index]["type"] = json_data["product-name"]
            data["records"][index]["version"] = json_data["product-version"]
            data["records"][index]["state"] = "OK"
            data["records"][index]["app"] = ""
            runningWar = "N/A"
            for index2, f2 in enumerate(json_data["deployment"], start=0):
                warRes = getState(f2,f["ip"]+":"+f["port"],f["username"],f["password"])
                if warRes == "true":
                    data["records"][index]["app"] = data["records"][index]["app"]+"<div style='padding:2px;'>"+f2+"</div>"
            data["records"][index]["username"] = ""
            data["records"][index]["password"] = ""
        except:
            data["records"][index]["name"] = "N/A"
            data["records"][index]["type"] = "N/A"
            data["records"][index]["version"] = "N/A"
            data["records"][index]["state"] = "NOK"
            data["records"][index]["app"] = "N/A"
            data["records"][index]["username"] = ""
            data["records"][index]["password"] = ""

    return Response(json.dumps(data), mimetype='application/json')
