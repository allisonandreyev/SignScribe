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

#grabs info from config file
exitWord, wordsPause, lettersPause, autoSave, filter1 = parserConfig.configParser()

wordBacklog = ["abcdefghijklmnopqrstuvwxyz"]
fullTranscript = []

GUI_text_queue = queue.Queue()
GUI_hand_queue = queue.Queue()

file2 = 'fullTranscript.txt'
file1 = 'CrossCommunication.txt'
ButtonPin = 24 # Should be 18
RGB_B = 17 # Should be 11
RGB_G = 27 # Should be 13
RGB_R = 22 # Should be 15


#vosk model
path=r'/home/signscribe/Downloads/SignScribe-master/Organization/VoskModels/vosk-model-small-en-us-0.15'

def Setup():
	#Where is the setmode it should be set to board but its set to GPIO...
    RPi.GPIO.setup(ButtonPin, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
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
	ExitButtonPressed = False
	
	recognizer = KaldiRecognizer(Model(path), 16000)

	stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

	stream.start_stream()
	
	print("Say exit when you want to terminate the program... \n")
	SetRGBColor(0, 100, 0)
	#reads data
	while True:
		data = stream.read(16000)
		
		if not RPi.GPIO.input(ButtonPin):
			print("Button Pressed")
			with open(file2, 'a') as f2:
				f2.write(str(fullTranscript) + '\n')
			print("Contents of text transcript have been automatically saved to ", file2)
			# stops data collection
			stream.stop_stream()
			stream.close()
			SetRGBColor(100, 0, 0)
			sleep(2)
			SetRGBColor(0, 0, 0)
			exit


		#clears cross communication file from previous use
		with open(file1, 'w') as file:
			pass

		#appends data to full transcript & word backlog
		if recognizer.AcceptWaveform(data) == True:
			result = recognizer.Result()
			result_dict = json.loads(result)
			text = result_dict.get("text","")
			newText = text.split()
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
			#appends cross communication.txt
			with open(file1, 'a') as f:
				f.write(str(wordBacklog) + '\n')

			#quits program if exit word has been stated & if autosave is True, appends full transcript to a file
			if exitWord in text.lower() or ExitButtonPressed == True:
				print("Exiting...\n")
				print("AUTOSAVE IS: ",autoSave)
				if autoSave == True:
					with open(file2, 'a') as f2:
						f2.write(str(fullTranscript) + '\n')
					print("Contents of text transcript have been automatically saved to ", file2)
					
				
					# stops data collection
					stream.stop_stream()
					stream.close()
					SetRGBColor(100, 0, 0)
					sleep(2)
					SetRGBColor(0, 0, 0)
					exit


def letterSwitch():
	sleep(2)
	stop = exitWord.split();
	while True:	
		sleep(wordsPause)
		#checks if the exit word has been spoken, if it has the hand will not sign it
		if not wordBacklog == [] and not set(stop).issubset(set(wordBacklog)) and wordBacklog[0] != "[censored]":
			for letter in wordBacklog[0]: 
				sleep(lettersPause)
				
				#disect word back log into letters & run appropriate function
				match letter:
					case 'a':
						controlServo(serv1 = 100, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('a')
					case 'b':
						controlServo(serv1 = 10, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10)
						GUI_hand_queue.put('b')
					case 'c':
						controlServo(serv1 = 80, serv2 = 80, serv3 = 80, serv4 = 80, serv5 = 80)
						GUI_hand_queue.put('c')
					case 'd':
						controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('d')
					case 'e':
						controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('e')
					case 'f':
						controlServo(serv1 = 10, serv2 = 160, serv3 = 10, serv4 = 10, serv5 = 10)
						GUI_hand_queue.put('f')
					case 'g':
						controlServo(serv1 = 80, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('g')
					case 'h':
						controlServo(serv1 = 10, serv2 = 10, serv3 = 10, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('h')
					case 'i':
						controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 10)
						GUI_hand_queue.put('i')
					case 'j':
						controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 10)
						sleep(lettersPause)
						controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160)
						sleep(lettersPause)
						controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 10)
						GUI_hand_queue.put('j')
					case 'k':
						controlServo(serv1 = 10, serv2 = 10, serv3 = 10, serv4 = 160, serv5 = 160)
						sleep(lettersPause)
						controlServo(serv1 = 10, serv2 = 10, serv3 = 10, serv4 = 160, serv5 = 160)
						sleep(lettersPause)
						controlServo(serv1 = 10, serv2 = 10, serv3 = 10, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('k')
					case 'l':
						controlServo(serv1 = 160, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('l')
					case 'm':
						controlServo(serv1 = 10, serv2 = 80, serv3 = 80, serv4 = 80, serv5 = 160)
						GUI_hand_queue.put('m')
					case 'n':
						controlServo(serv1 = 10, serv2 = 80, serv3 = 80, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('n')
					case 'o':
						controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('o')
					case 'p':
						controlServo(serv1 = 80, serv2 = 10, serv3 = 100, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('p')
					case 'q':
						controlServo(serv1 = 80, serv2 = 80, serv3 = 160, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('q')
					case 'r':
						controlServo(serv1 = 10, serv2 = 40, serv3 = 40, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('r')
					case 's':
						controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160)
						sleep(lettersPause)
						controlServo(serv1 = 160, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160)
						sleep(lettersPause)
						controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('s')
					case 't':
						controlServo(serv1 = 160, serv2 = 80, serv3 = 160, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('t')
					case 'u':
						controlServo(serv1 = 60, serv2 = 10, serv3 = 10, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('u')
					case 'v':
						controlServo(serv1 = 10, serv2 = 10, serv3 = 10, serv4 = 160, serv5 = 160)
						sleep(lettersPause)
						controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160)
						sleep(lettersPause)
						controlServo(serv1 = 10, serv2 = 10, serv3 = 10, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('v')
					case 'w':
						controlServo(serv1 = 10, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 160)
						GUI_hand_queue.put('w')
					case 'x':
						controlServo(serv1 = 10, serv2 = 80, serv3 = 160, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('x')
					case 'y':
						controlServo(serv1 = 160, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 10)
						GUI_hand_queue.put('y')
					case 'z':
						controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160)
						GUI_hand_queue.put('z')
			print(" ")
			controlServo(serv1 = 160, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10)
			sleep(lettersPause)
		elif not wordBacklog == [] and wordBacklog[0] == "[censored]":
			controlServo(serv1 = 160, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10)
			sleep(0.2)
			controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160)
			sleep(0.2)
			controlServo(serv1 = 160, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10)			
			sleep(0.2)
			controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160)
			sleep(0.2)
			controlServo(serv1 = 160, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10)	
		if not wordBacklog == []:
			wordBacklog.remove(wordBacklog[0])
			
#reset to default position
Setup()
sleep(2)
SetRGBColor(0, 0, 100)
controlServo(serv1 = 160, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10)
sleep(2)


#initiate and run threading (multiprocessing)
GUI_Thread = thread.Thread(target=UI_Stuff.GUI_APP,args=[GUI_text_queue, wordBacklog, GUI_hand_queue])
ServoThread = thread.Thread(target=letterSwitch)
VoiceThread = thread.Thread(target=VoiceToText)

GUI_Thread.start()
ServoThread.start()
VoiceThread.start()

GUI_Thread.join()
ServoThread.join()
VoiceThread.join()
