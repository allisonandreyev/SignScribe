from vosk import Model, KaldiRecognizer
from time import sleep
import pyaudio
import json
import thread
import RPi.GPIO
import parserConfig
from HandControl import controlServo
import queue
import UI_Stuff
import math

#grabs info from config file using the configParser() function and assigns to variables
exitWord, wordsPause, lettersPause, autoSave, filter1, autoLaunch = parserConfig.configParser()

#initializes variables and queue
wordBacklog = ["abcdefghijklmnopqrstuvwxyz"]
fullTranscript = []

GUI_text_queue = queue.Queue()
GUI_hand_queue = queue.Queue()

#creates file names
file2 = 'fullTranscript.txt'
"""
ButtonPin = 24 # Should be 18
"""
#LED light color configuration
RGB_B = 17 # Should be 11
RGB_G = 27 # Should be 13
RGB_R = 22 # Should be 15


#vosk model path (SHOULD BE CHANGED)
path=r'/home/signscribe/Downloads/SignScribe-master/Organization/VoskModels/vosk-model-small-en-us-0.15'

def Setup():
	#Where is the setmode it should be set to board but its set to GPIO...
    """
    RPi.GPIO.setup(ButtonPin, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
    """
    RPi.GPIO.setup(RGB_B, RPi.GPIO.OUT)
    RPi.GPIO.setup(RGB_G, RPi.GPIO.OUT)
    RPi.GPIO.setup(RGB_R, RPi.GPIO.OUT)
    RPi.GPIO.output(RGB_B, RPi.GPIO.HIGH)
    RPi.GPIO.output(RGB_G, RPi.GPIO.HIGH)
    RPi.GPIO.output(RGB_R, RPi.GPIO.HIGH)
    global RL
    global GL
    global BL
    RL = RPi.GPIO.PWM(RGB_R, 2000)
    GL = RPi.GPIO.PWM(RGB_G, 1999)
    BL = RPi.GPIO.PWM(RGB_B, 5000)
    RL.start(100)
    GL.start(100)
    BL.start(100)
    
def SetRGBColor(Red, Green, Blue):
    InvRed = 100 - Red
    InvGreen = 100 - Green
    InvBlue = 100 - Blue
    RL.ChangeDutyCycle(InvRed)
    GL.ChangeDutyCycle(InvGreen)
    BL.ChangeDutyCycle(InvBlue)


def VoiceToText():

	#Opens and sets up live audio streaming
	ExitButtonPressed = False
	
	recognizer = KaldiRecognizer(Model(path), 16000)

	stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

	stream.start_stream()
	
	print("Say exit when you want to terminate the program... \n")
	SetRGBColor(0, 100, 0)
	
	#reads data and uses vosk to interpret text
	while True:
		data = stream.read(16000)
		
		"""
		if not RPi.GPIO.input(ButtonPin):
			print("Button Pressed")
			with open(file2, 'a') as f2:
				f2.write(str(fullTranscript) + '\n')
			print("Contents of text transcript have been automatically saved to ", file2)
			# stops data collection
			SetRGBColor(100, 0, 0)
			stream.stop_stream()
			stream.close()
			sleep(2)
			SetRGBColor(0, 0, 0)
			exit
		"""

		#appends data to full transcript & word backlog IF the data is valid
		if recognizer.AcceptWaveform(data) == True:
			result = recognizer.Result()
			result_dict = json.loads(result)
			text = result_dict.get("text","")
			newText = text.split()
			#appends new text to work backlog and full transcript, if the word is censored, it appends "[censored]" instead
			for i in newText:
				if i not in filter1:
					wordBacklog.append(i)
					fullTranscript.append(i)
				else:
					wordBacklog.append("[censored]")
					fullTranscript.append("[censored]")
				GUI_text_queue.put(' '.join(wordBacklog))

			#outputs word backlog (for debugging purposes)
			if not wordBacklog == []:
				print(str(wordBacklog))

			#quits program if exit word has been stated
				if exitWord in text.lower() or ExitButtonPressed == True:
					#prints status
					print("Exiting...\n")
					print("AUTOSAVE IS: ",autoSave)
					# if autosave is True, appends full transcript to a file
					if autoSave == True:
						with open(file2, 'a') as f2:
							f2.write(str(fullTranscript) + '\n')
						print("Contents of text transcript have been automatically saved to ", file2)
						
					
					# Stops data collection and sets RGB to turn off
					SetRGBColor(100, 0, 0)
					stream.stop_stream()
					stream.close()
					sleep(2)
					SetRGBColor(0, 0, 0)
					exit()

#switch statement which signs letter
def letterSwitch():
	sleep(2)
	stop = exitWord.split();
	
	while True:	
		sleep(wordsPause)
		
		#checks if the exit word has been spoken, if it has the hand will not sign it
		if not wordBacklog == [] and not set(stop).issubset(set(wordBacklog)) and wordBacklog[0] != "[censored]":
			for letter in wordBacklog[0]: 
				
				#disect word backlog into letters & run appropriate function based on letter kind
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
						controlServo(serv1 = 80, serv2 = 120, serv3 = 120, serv4 = 120, serv5 = 120, serv6 = 180, serv7 = 90)
						GUI_hand_queue.put('c')
						sleep(lettersPause)
					case 'd':
						controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 180, serv7 = 90)
						GUI_hand_queue.put('d')
						sleep(lettersPause)
					case 'e':
						controlServo(serv1 = 50, serv2 = 140, serv3 = 140, serv4 = 125, serv5 = 120, serv6 = 90, serv7 = 90)
						GUI_hand_queue.put('e')
						sleep(lettersPause)
					case 'f':
						controlServo(serv1 = 10, serv2 = 160, serv3 = 10, serv4 = 10, serv5 = 10, serv6 = 180, serv7 = 90)
						GUI_hand_queue.put('f')
						sleep(lettersPause)
					case 'g':
						controlServo(serv1 = 80, serv2 = 40, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 180, serv7 = 180)
						GUI_hand_queue.put('g')
						sleep(lettersPause)
					case 'h':
						controlServo(serv1 = 80, serv2 = 40, serv3 = 60, serv4 = 160, serv5 = 160, serv6 = 180, serv7 = 180)
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
						sleep(lettersPause-0.3)
					case 'k':
						controlServo(serv1 = 10, serv2 = 10, serv3 = 110, serv4 = 160, serv5 = 160, serv6 = 180, serv7 = 90)
						GUI_hand_queue.put('k')
						sleep(lettersPause)
					case 'l':
						controlServo(serv1 = 160, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 180, serv7 = 90)
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
						controlServo(serv1 = 30, serv2 = 140, serv3 = 140, serv4 = 140, serv5 = 140, serv6 = 180, serv7 = 90)
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
						controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 10, serv5 = 160, serv6 = 90, serv7 = 90)
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
						sleep(0.1)
						controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 15, serv7 = 120)
						sleep(0.1)
						controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 165, serv7 = 120)
						sleep(0.1)
						controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 60, serv7 = 160)
						sleep(0.1)
						controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 120, serv7 = 160)
						GUI_hand_queue.put('z')
						sleep(lettersPause-0.4)

			#signs space character (high five position) after every word
			controlServo(serv1 = 160, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10, serv6 = 90, serv7 = 90)
			
			#GUI_hand_queue.put(' ')
			
			#pause amount between each word which is adjusted in CONFIG file
			sleep(lettersPause)
		
		#adjusts how the hand signs a censored word. Currently the hand skips over it, but that can be changed here:
		"""
		elif not wordBacklog == [] and wordBacklog[0] == "[censored]":
			controlServo(serv1 = 160, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10, serv6 = 90, serv7 = 90)
			sleep(lettersPause)	
			controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
			sleep(lettersPause)	
			controlServo(serv1 = 160, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10, serv6 = 90, serv7 = 90)			
			sleep(lettersPause)	
			controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
			sleep(lettersPause)	
			controlServo(serv1 = 160, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10, serv6 = 90, serv7 = 90)
			sleep(wordsPause)
		"""
		if not wordBacklog == []:
			wordBacklog.remove(wordBacklog[0])
			
#reset to the default position
Setup()
sleep(2)
SetRGBColor(0, 0, 100)
controlServo(serv1 = 160, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10, serv6 = 90, serv7 = 90)
sleep(2)

#initiate and run threading (multiprocessing)

#sets lettersPause to .4 if it is less
if not lettersPause >= 0.4:
	lettersPause = 0.4

if autoLaunch == "True":
	GUI_Thread = thread.Thread(target=UI_Stuff.GUI_APP,args=[GUI_text_queue, wordBacklog, GUI_hand_queue])
ServoThread = thread.Thread(target=letterSwitch)
VoiceThread = thread.Thread(target=VoiceToText)

if autoLaunch == "True":
	GUI_Thread.start()
ServoThread.start()
VoiceThread.start()

if autoLaunch == "True":
	GUI_Thread.join()
ServoThread.join()
VoiceThread.join()
