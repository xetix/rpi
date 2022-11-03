from contextlib import nullcontext
import pyrebase
from time import gmtime, strftime

def firebase_init(email, password):
    config = {
        "apiKey": "AIzaSyAFk8mE_XThMws4T3dJZ1mrw_fWHDvVL4c",
        "authDomain": "szakdolgozat-7f935.firebaseapp.com",
        "databaseURL": "https://szakdolgozat-7f935-default-rtdb.europe-west1.firebasedatabase.app",
        "projectId": "szakdolgozat-7f935",
        "storageBucket": "szakdolgozat-7f935.appspot.com",
        "messagingSenderId": "290028249829",
        "appId": "1:290028249829:web:36e50c40b4e28b12c7aa0c"
    }

    global firebase
    firebase = pyrebase.initialize_app(config)
    global auth 
    auth = firebase.auth()
    global user
    user = auth.sign_in_with_email_and_password(email, password)
    global db
    db = firebase.database()
    refreshToken()

def refreshToken():
    global user
    user = auth.refresh(user['refreshToken'])

def getSp():
    v = db.child(user['userId']).child("controll").child("setpoint").get(user['idToken'])
    return float(v.val())

def getManualMode():
    v = db.child(user['userId']).child("controll").child("manual_mode").get(user['idToken'])
    return bool(v.val())

def getPriorityOn():
    v = db.child(user['userId']).child("controll").child("priority_on").get(user['idToken'])
    return bool(v.val())

def getHys():
    v = db.child(user['userId']).child("controll").child("hysteresis").get(user['idToken'])
    return float(v.val())

def getSyn():
    v = db.child(user['userId']).child("syncron").child("syn").get(user['idToken'])
    return bool(v.val())

def getPrograms():
    v = db.child(user['userId']).child("programs").get(user['idToken'])
    return v.val()

def setAck( value ):
    data = {
        "ack": bool(value)
    }
    db.child(user['userId']).child("syncron").update(data, user['idToken'])

def setMeassuredValue( value, status ):
    timeStemp = strftime("%Y.%m.%d. %H:%M:%S", gmtime())
    data = {
        "time": timeStemp,
        "value": float(value),
        "status": bool(status)
    }
    db.child(user['userId']).child("meassure").update(data, user['idToken'])
