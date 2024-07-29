from adafruit_servokit import ServoKit
from time import sleep

ServoController = ServoKit(channels = 16)

while True:
	for i in range(16):
		sleep(0.005)
		ServoController.servo[i].angle = 0
	sleep(0.5)
	for i in range(16):
		sleep(0.005)
		ServoController.servo[i].angle = 120
	sleep(0.5)


