import RPi.GPIO
from adafruit_servokit import ServoKit

ServoController = ServoKit(channels = 16)

# function definition. This function takes in the angle measurements for all 7 servo movements, with default values being the high five position and controls the servos to move to that angle position.
# default values can be changed, but must be 10 <= X <= 170 or the servos will be stressed.
def controlServo(serv1 = 0, serv2 = 0, serv3 = 0, serv4 = 0, serv5 = 0, serv6 = 90, serv7 = 90):
	ServoController.servo[1].angle = serv1
	ServoController.servo[2].angle = serv2
	ServoController.servo[3].angle = serv3
	ServoController.servo[4].angle = serv4
	ServoController.servo[5].angle = serv5
	ServoController.servo[6].angle = serv6
	ServoController.servo[7].angle = serv7

#calls the function for testing, now used in SignScribeOfficial.py file
#controlServo(serv1 = 160, serv2 = 0, serv3 = 0, serv4 = 0, serv5 = 0, serv6 = 90, serv7 = 90)
