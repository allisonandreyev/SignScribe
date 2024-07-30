import RPi.GPIO as GPIO
from time import sleep

BtnPin = 37

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.add_event_detect(BtnPin, GPIO.BOTH, callback=detect, bouncetime=200)

def detect(chn):
    print(GPIO.input(BtnPin))

def loop():
    while True:
        sleep(0.1)

setup()
sleep(0.5)
loop()
