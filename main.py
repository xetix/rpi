import time
import datetime
from temp import read_temp
from fbd import *
from lcd import clearLCD, outToLCD
from led import led
from programicalSp import getProgramicalSp
import atexit

setPoint = 22
activeSp = setPoint
hyst = 0.5
limit = 40.0

on = False
typeTxt = "?"
syn = False
storeValue = 0
storeState = None
syncDatasTime = 9
updateTokenTime = 50*60

firebase_init("kovacsgergo8303@gmail.com","jelszo_1324")

lastRefreshDatas = datetime.datetime.now()
lastRefreshToken = lastRefreshDatas

def exit_handler():
    led(False)
    clearLCD()
    print('A termosztát funkció leállt.')

atexit.register(exit_handler)

def getDatas():
    global activeSp
    global typeTxt
    global hyst
    global syn
    setPoint = getSp()
    hyst = getHys()
    programs = getPrograms()
    programicalSp = getProgramicalSp(programs)
    if(programicalSp == None):
        programicalSp = setPoint
    priority = getPriorityOn()
    manual = getManualMode()
    syn = getSyn()
    if(priority):
        activeSp = limit
        typeTxt = "D"
    elif(not manual):
        activeSp = programicalSp
        typeTxt = "P"
    else:
        activeSp = setPoint
        typeTxt = "K"
    if(syn):
            setAck(True)

getDatas()

while True:
    actualTemp = read_temp()
    actualTime = datetime.datetime.now()

    deltaRefreshDatas = actualTime-lastRefreshDatas
    if(deltaRefreshDatas.total_seconds() >=  syncDatasTime):
        getDatas()        
        lastRefreshDatas = actualTime

    deltaRefreshToken = actualTime-lastRefreshToken
    if(deltaRefreshToken.total_seconds() >= updateTokenTime):
        refreshToken()
        deltaRefreshToken = actualTime

    on = ( actualTemp < activeSp-hyst )

    print('Aktuális hőfok: '+str(actualTemp)+'°C, Szetpont: '+str(typeTxt)+str(activeSp)+\
        '°C, Hiszterézis: '+str(hyst)+'°C, Fűtés: '+( 'Be' if on else 'Ki' ), end="\r")
    led(on)
    outToLCD( actualTemp, on, activeSp, hyst, typeTxt )

    if((actualTemp != storeValue) or (on != storeState)):
        storeValue = actualTemp
        storeState = on
        setMeassuredValue(float(actualTemp),bool(on))
