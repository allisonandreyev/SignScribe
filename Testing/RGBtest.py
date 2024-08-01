#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]
R = 15
G = 13
B = 11

def setup(Rpin, Gpin, Bpin):
   global pins
   global p_R, p_G, p_B
   pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
   GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
   for i in pins:
      GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
      GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led

   p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
   p_G = GPIO.PWM(pins['pin_G'], 1999)
   p_B = GPIO.PWM(pins['pin_B'], 5000)

   p_R.start(100)      # Initial duty Cycle = 0(leds off)
   p_G.start(100)
   p_B.start(100)

def loop():
   while True:
       p_R.ChangeDutyCycle(100)
       p_G.ChangeDutyCycle(0)
       p_B.ChangeDutyCycle(100)
       time.sleep(1)

setup(R, G, B)
loop()
