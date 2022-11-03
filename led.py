import RPi.GPIO as GPIO

ledPin = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.HIGH)

def led(on):
    if on :
        GPIO.output(ledPin, GPIO.LOW)
    else:
        GPIO.output(ledPin, GPIO.HIGH)