from flask import Flask, jsonify, request
import pymongo, os 
from dotenv import load_dotenv
import requests
from flask_jwt_extended import create_access_token, JWTManager, jwt_required
load_dotenv()
import datetime
import socket

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('secret_key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(weeks=8)
JWTManager(app)
server = pymongo.MongoClient(os.getenv('mongoclient'))
db = server['db']
user = db['users']
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

# @app.route('/')
# def home():
#     user.insert_one({'id':1000})
#     return {'status':2}

@app.post('/api/register')
def register():
    data = request.get_json()
    username = data['username']
    comapny_name = data['company_name']
    profession = data['profession']
    password = data['password']
    user.insert_one({'username' : username,
                    'company_name' :comapny_name,
                    'profession' : profession,
                    'password' : password,
                    'type':'users'
                    })
    return {'status':True, 'message':'User Registered'}


@app.post('/api/login')
def login():
    data = request.get_json()
    exist_user = user.find_one({'username':data['name'], 'password':data['password']},{'_id':0})
    # print(exist_user)
    if exist_user:
        access_token = create_access_token(identity=10, additional_claims={'role':exist_user['type']})
        return { 'status':True, 'token':access_token, 'role':exist_user['type'] }
    return {'status':False}

@app.route('/api/alerts')
@jwt_required()
def alerts():
    return {'status':True}

@app.route('/api/Allalertsdetails')
def AllAlertDetails():
    response = requests.get('https://sachet.ndma.gov.in/cap_public_website/FetchAllAlertDetails').json()
    return response

@app.get('/api/Statewisedetails')
def StateWiseDetails():
    response = requests.get('https://sachet.ndma.gov.in/cap_public_website/FetchDashboardData').json()
    return response

@app.route('/api/localstate')
def LocalState():
    response = requests.get('https://sachet.ndma.gov.in/locales/en/state.json').json()
    return response

@app.route('/api/earthquake')
def EarthQuake():
    response = requests.get('https://sachet.ndma.gov.in/cap_public_website/FetchEarthquakeAlerts').json()
    return response

@app.route('/api/viewpointlink')
def viewpointlink():
    response = requests.get('https://maps.googleapis.com/$rpc/google.internal.maps.mapsjs.v1.MapsJsInternalService/GetViewportInfo').json()
    return response

if __name__=="__main__":
    print(IPAddr)
    app.run(debug=True ,host='192.168.0.138')