from adafruit_servokit import ServoKit
from time import sleep
from HandControlTest import controlServo

letter = ''
	
sleep(1)
controlServo(160, 0, 0, 0, 0, 0, 40, 20)

	
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
		controlServo(10, 160, 160, 160, 10)
		sleep(0.4)
		controlServo(10, 160, 160, 160, 160)
		sleep(0.4)
		controlServo(10, 160, 160, 160, 10)
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
