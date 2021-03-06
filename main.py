from flask import Flask, render_template, request, Response, jsonify
import requests
from requests.auth import HTTPDigestAuth
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import ImmutableMultiDict
import urllib
import json
import base64

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
    warName = urllib.parse.quote_plus(warName)
    url = "http://"+ip+"/management/deployment/"+warName+"?operation=attribute&name=enabled"
    r = requests.get(url,
                     proxies={"http": "http://10.0.144.183:8080"},
                     auth=HTTPDigestAuth(username, password)
                     )
    return r.text

@app.route('/deploy', methods=['POST'])
def deploy():
    content = request.form.get('content')
    dataContent = base64.b64decode(content)
    url = request.form.get('url')
    url = url+"/management"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url,
        data = dataContent,
        proxies={"http": "http://10.0.144.183:8080"},
        auth=HTTPDigestAuth('sigit', 'sigit'),
        headers=headers
    )
    return r.content

@app.route('/undeploy', methods=['POST'])
def undeploy():
    content = request.form.get('content')
    dataContent = base64.b64decode(content)
    url = request.form.get('url')
    url = url+"/management"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url,
        data = dataContent,
        proxies={"http": "http://10.0.144.183:8080"},
        auth=HTTPDigestAuth('sigit', 'sigit'),
        headers=headers
    )
    return r.content

@app.route('/remove', methods=['POST'])
def remove():
    content = request.form.get('content')
    dataContent = base64.b64decode(content)
    url = request.form.get('url')
    url = url+"/management"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url,
        data = dataContent,
        proxies={"http": "http://10.0.144.183:8080"},
        auth=HTTPDigestAuth('sigit', 'sigit'),
        headers=headers
    )
    return r.content

@app.route('/results')
def results():
    with open("config.json", 'r') as file:
        data = file.read()
    data = json.loads(data)
    records = data["records"]

    for index,f in enumerate(records, start=0):
        try:
            res = load(f["ip"]+":"+f["port"],f["username"],f["password"])
            json_data = json.loads(res)
            idCom = data["records"][index]["ip"].replace(".","")+data["records"][index]["port"]+"_"+str(index)
            data["records"][index]["id"] = "WAR_"+idCom
            data["records"][index]["name"] = json_data["name"]
            data["records"][index]["type"] = json_data["product-name"]
            data["records"][index]["version"] = json_data["product-version"]
            data["records"][index]["state"] = "OK"
            data["records"][index]["app"] = ""
            runningWar = "N/A"
            for index2, f2 in enumerate(json_data["deployment"], start=0):
                warRes = getState(f2,f["ip"]+":"+f["port"],f["username"],f["password"])
                #if warRes == "true":
                data["records"][index]["app"] = data["records"][index]["app"]+warRes+"~"+f2+"###"
            data["records"][index]["username"] = ""
            data["records"][index]["password"] = ""
        except:
            idCom = data["records"][index]["ip"].replace(".","")+data["records"][index]["port"]+"_"+str(index)
            data["records"][index]["id"] = "WAR_"+idCom
            data["records"][index]["name"] = "N/A"
            data["records"][index]["type"] = "N/A"
            data["records"][index]["version"] = "N/A"
            data["records"][index]["state"] = "NOK"
            data["records"][index]["app"] = "N/A"
            data["records"][index]["username"] = ""
            data["records"][index]["password"] = ""

    return Response(json.dumps(data), mimetype='application/json')