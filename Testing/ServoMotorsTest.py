from adafruit_servokit import ServoKit
from time import sleep
from HandControlTest import controlServo

letter = 'z'
	
match letter:
	case 'a':
		controlServo(100, 160, 160, 160, 160)
	case 'b':
		controlServo(10,10,10,10,10)
	case 'c':
		controlServo(80, 80, 80, 80, 80)
	case 'd':
		controlServo(10, 10, 160, 160, 160)
	case 'e':
		controlServo(10, 160, 160, 160, 160)
	case 'f':
		controlServo(10, 160, 10, 10, 10)
	case 'g':
		controlServo(80, 10, 160, 160, 160)
	case 'h':
		controlServo(10, 10, 10, 160, 160)
	case 'i':
		controlServo(10, 160, 160, 160, 10)
	case 'j':
		controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 10, serv6 = 90, serv7 = 90, serv8 = 90)
		sleep(0.1)
		controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 10, serv6 = 90, serv7 = 160, serv8 = 90)
		sleep(0.1)
		controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 10, serv6 = 35, serv7 = 160, serv8 = 90)
		sleep(0.1)
		controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 10, serv6 = 35, serv7 = 140, serv8 = 90)
		sleep(0.1)
	case 'k':
		controlServo(10, 10, 10, 160, 160)
		sleep(0.4)
		controlServo(10, 10, 10, 160, 160)
		sleep(0.4)
		controlServo(10, 10, 10, 160, 160)
	case 'l':
		controlServo(160, 10, 160, 160, 160)
	case 'm':
		controlServo(10, 80, 80, 80, 160)
	case 'n':
		controlServo(10, 80, 80, 160, 160)
	case 'o':
		controlServo(10, 160, 160, 160, 160)
	case 'p':
		controlServo(80, 10, 100, 160, 160)
	case 'q':
		controlServo(80, 80, 160, 160, 160)
	case 'r':
		controlServo(10, 40, 40, 160, 160)
	case 's':
		controlServo(10, 160, 160, 160, 160)
		sleep(0.4)
		controlServo(160, 160, 160, 160, 160)
		sleep(0.4)
		controlServo(10, 160, 160, 160, 160)
	case 't':
		controlServo(160, 80, 160, 160, 160)
	case 'u':
		controlServo(60, 10, 10, 160, 160)
	case 'v':
		controlServo(10, 10, 10, 160, 160)
		sleep(0.4)
		controlServo(10, 160, 160, 160, 160)
		sleep(0.4)
		controlServo(10, 10, 10, 160, 160)
	case 'w':
		controlServo(10, 10, 10, 10, 160)
	case 'x':
		controlServo(10, 80, 160, 160, 160)
	case 'y':
		controlServo(160, 160, 160, 160, 10)
	case 'z':
		controlServo(10, 10, 160, 160, 160)
	case _:
		sleep(0.005)

sleep(6)
