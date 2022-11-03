import RPi.GPIO as GPIO
import LiquidCrystalPi
import time as time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

LCD = LiquidCrystalPi.LCD(29, 31, 33, 35, 37, 38)

LCD.begin(16,2)
LCD.clear()

def clearLCD():
    LCD.begin(16,2)
    LCD.clear()

def outToLCD( temp, state, setpoint, hysteresis, typeTxt ):
    line1 = ("Temp:{f_act:.1f}ßC,  "+( 'Be' if state else 'Ki' )).format(f_act = temp)
    line2 = "SP:"+str(typeTxt[0])+"{f_sp:.1f}ßC,{f_hys:.1f}ßC".format(f_sp = setpoint, f_hys = hysteresis)
    lcdPrint(line1,line2)

def lcdPrint(line1 = "",line2 = ""):
    LCD.clear()
    LCD.home();
    LCD.write(line1)
    LCD.nextline()
    LCD.write(line2)    