import RPi.GPIO
from adafruit_servokit import ServoKit

ServoController = ServoKit(channels = 16)

def controlServo(serv1 = 0, serv2 = 0, serv3 = 0, serv4 = 0, serv5 = 0, serv6 = 90, serv7 = 90):
	ServoController.servo[1].angle = serv1
	ServoController.servo[2].angle = serv2
	ServoController.servo[3].angle = serv3
	ServoController.servo[4].angle = serv4
	ServoController.servo[5].angle = serv5
	ServoController.servo[6].angle = serv6
	ServoController.servo[7].angle = serv7
	
#controlServo(serv1 = 160, serv2 = 0, serv3 = 0, serv4 = 0, serv5 = 0, serv6 = 90, serv7 = 90)
