import RPi.GPIO
from adafruit_servokit import ServoKit

ServoController = ServoKit(channels = 16)


def controlServo(serv1 = 0, serv2 = 0, serv3 = 0, serv4 = 0, serv5 = 0, serv8 = 0, serv9 = 0, serv10 = 0):
	ServoController.servo[1].angle = serv1
	ServoController.servo[2].angle = serv2
	ServoController.servo[3].angle = serv3
	ServoController.servo[4].angle = serv4
	ServoController.servo[5].angle = serv5
	ServoController.servo[8].angle = serv8
	ServoController.servo[9].angle = serv9
	ServoController.servo[10].angle = serv10
