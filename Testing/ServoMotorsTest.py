from adafruit_servokit import ServoKit
from time import sleep
from HandControlTest import controlServo

letter = 'z'
	
match letter:
	case 'a':
		controlServo(serv1 = 100, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('a')
		sleep(lettersPause)
	case 'b':
		controlServo(serv1 = 10, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('b')
		sleep(lettersPause)
	case 'c':
		controlServo(serv1 = 80, serv2 = 120, serv3 = 120, serv4 = 120, serv5 = 120, serv6 = 0, serv7 = 90)
		GUI_hand_queue.put('c')
		sleep(lettersPause)
	case 'd':
		controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 0, serv7 = 90)
		GUI_hand_queue.put('d')
		sleep(lettersPause)
	case 'e':
		controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('e')
		sleep(lettersPause)
	case 'f':
		controlServo(serv1 = 10, serv2 = 160, serv3 = 10, serv4 = 10, serv5 = 10, serv6 = 0, serv7 = 90)
		GUI_hand_queue.put('f')
		sleep(lettersPause)
	case 'g':
		controlServo(serv1 = 80, serv2 = 40, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 0, serv7 = 180)
		GUI_hand_queue.put('g')
		sleep(lettersPause)
	case 'h':
		controlServo(serv1 = 80, serv2 = 40, serv3 = 60, serv4 = 160, serv5 = 160, serv6 = 0, serv7 = 180)
		GUI_hand_queue.put('h')
		sleep(lettersPause)
	case 'i':
		controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 10, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('i')
		sleep(lettersPause)
	case 'j':
		controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 10, serv6 = 90, serv7 = 90)
		sleep(0.1)
		controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 10, serv6 = 90, serv7 = 160)
		sleep(0.1)
		controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 10, serv6 = 35, serv7 = 160)
		sleep(0.1)
		controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 10, serv6 = 35, serv7 = 140)
		GUI_hand_queue.put('j')
		sleep(lettersPause)
	case 'k':
		controlServo(serv1 = 10, serv2 = 10, serv3 = 110, serv4 = 160, serv5 = 160, serv6 = 0, serv7 = 90)
		GUI_hand_queue.put('k')
		sleep(lettersPause)
	case 'l':
		controlServo(serv1 = 160, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('l')
		sleep(lettersPause)
	case 'm':
		controlServo(serv1 = 10, serv2 = 80, serv3 = 80, serv4 = 80, serv5 = 160, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('m')
		sleep(lettersPause)
	case 'n':
		controlServo(serv1 = 10, serv2 = 80, serv3 = 80, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('n')
		sleep(lettersPause)
	case 'o':
		controlServo(serv1 = 30, serv2 = 140, serv3 = 140, serv4 = 140, serv5 = 140, serv6 = 0, serv7 = 90)
		GUI_hand_queue.put('o')
		sleep(lettersPause)
	case 'p':
		controlServo(serv1 = 10, serv2 = 10, serv3 = 100, serv4 = 160, serv5 = 160, serv6 = 180, serv7 = 180)
		GUI_hand_queue.put('p')
		sleep(lettersPause)
	case 'q':
		controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 180, serv7 = 180)
		GUI_hand_queue.put('q')
		sleep(lettersPause)
	case 'r':
		controlServo(serv1 = 10, serv2 = 40, serv3 = 40, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('r')
		sleep(lettersPause)
	case 's':
		controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
		sleep(0.2)
		controlServo(serv1 = 160, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
		sleep(0.2)
		controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('s')
		sleep(lettersPause)
	case 't':
		controlServo(serv1 = 160, serv2 = 80, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('t')
		sleep(lettersPause)
	case 'u':
		controlServo(serv1 = 60, serv2 = 10, serv3 = 10, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('u')
		sleep(lettersPause)
	case 'v':
		controlServo(serv1 = 10, serv2 = 10, serv3 = 10, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
		sleep(0.2)
		controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
		sleep(0.2)
		controlServo(serv1 = 10, serv2 = 10, serv3 = 10, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('v')
		sleep(lettersPause)
	case 'w':
		controlServo(serv1 = 10, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 160, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('w')
		sleep(lettersPause)
	case 'x':
		controlServo(serv1 = 10, serv2 = 80, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('x')
		sleep(lettersPause)
	case 'y':
		controlServo(serv1 = 160, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 10, serv6 = 90, serv7 = 90)
		GUI_hand_queue.put('y')
		sleep(lettersPause)
	case 'z':
		controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 15, serv7 = 120)
		sleep(0.1)
		controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 165, serv7 = 120)
		sleep(0.1)
		controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 60, serv7 = 160)
		sleep(0.2)
		controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 120, serv7 = 160)
		GUI_hand_queue.put('z')
		sleep(lettersPause)

#controlServo(serv1 = 100, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)

sleep(6)
