'''
MIT License

Copyright (c) 2024 SignScribe Allison Andreyev, Yenni Do, Elliott Owens, Sakib Niaz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
'''
from vosk import Model, KaldiRecognizer
from time import sleep
import pyaudio
import json
import thread
import RPi.GPIO
import parserConfig
from HandControl import controlServo
import queue
import InterfaceMain
import math

'''
exitWord - is the user-defined speech that terminates the program
wordPause - user defined stint between each word processed
lettersPause - user defined stint between each letter 
autoSave - a True or False value that determines whether or not all text will be recorded to fullTranscript
censorFilter - a user-defined list of words to be censors when captured by vosk
autoLaunch - a True or False value that determines whether or not the GUI will automatically launch
parserConfig - a function that read Config.txt in order to get uder-defined values as previously mentioned
'''
exitWord, wordsPause, lettersPause, autoSave, censorFilter, autoLaunch = parserConfig.configParser()

'''
wordBacklog - a list that captures the text to be processed through vosk. As soon as a
word is finished being signed by the robot, said word is deprecated from wordBacklog. The reverse is 
true when new text is captured by vosk

fullTranscript - a list that captures the text captured from vosk into a, however unlike wordBacklog, 
it does not deprecate text 
'''
wordBacklog = ["abcdefghijklmnopqrstuvwxyz"]
fullTranscript = []

'''
GUI_text_queue - a multi-threading stack that allows the program to communicate the contents of wordBacklog to GUI
GUI_hand_queue - a multi-threading stakc that allows the program to communcate the current letter being signed to GUI
'''
GUI_text_queue = queue.Queue()
GUI_hand_queue = queue.Queue()

'''
file2 - is the name of the file that saves the contents of fullTranscripts.
This allows for the program to save a log of all text ever captured by vosk with the permission of autoSave
'''
file2 = 'fullTranscript.txt'

"""
ButtonPin = 24 # Should be 18
"""
RGB_B = 17 # Should be 11
RGB_G = 27 # Should be 13
RGB_R = 22 # Should be 15

'''
path - is the directory path to the premade vosk model that the program uses.
We chose this model due to it's lightweight nature which is perfect for pi
'''
path=r'/home/signscribe/Downloads/SignScribe-master/Organization/VoskModels/vosk-model-small-en-us-0.15'

'''
Setup - is where the GPIO pins are setup to control the RGB LED and optionaly, the button.
'''
def Setup():
	
    '''
    Sets the mode of the specific raspberry pi pins for their corresponding function.
    '''
    """
    RPi.GPIO.setup(ButtonPin, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
    """
    RPi.GPIO.setup(RGB_B, RPi.GPIO.OUT)
    RPi.GPIO.setup(RGB_G, RPi.GPIO.OUT)
    RPi.GPIO.setup(RGB_R, RPi.GPIO.OUT)

    '''
    Sets the original state of the RGB LED GPIO pins.
    '''
    RPi.GPIO.output(RGB_B, RPi.GPIO.HIGH)
    RPi.GPIO.output(RGB_G, RPi.GPIO.HIGH)
    RPi.GPIO.output(RGB_R, RPi.GPIO.HIGH)

    '''
    Creates global variables to allow control of RBG using PWM in other functions.
    '''
    global RL
    global GL
    global BL
    RL = RPi.GPIO.PWM(RGB_R, 2000)
    GL = RPi.GPIO.PWM(RGB_G, 1999)
    BL = RPi.GPIO.PWM(RGB_B, 5000)

    '''
    Begins RGB LED with the color blue to indicate that the code is starting but not ready yet.
    '''
    RL.start(100)
    GL.start(100)
    BL.start(100)
    

'''
SetRGBColor - Function used to simplify setting the RGB LED to a different color from a range of 0-100.
'''
def SetRGBColor(Red, Green, Blue):
	
    '''
    Inverts the inputted value to the corresponding value for the RGB LED.
    '''
    InvRed = 100 - Red
    InvGreen = 100 - Green
    InvBlue = 100 - Blue

    '''
    Sets each of the 3 LEDs in the RGB LED to their corresponding values.
    '''
    RL.ChangeDutyCycle(InvRed)
    GL.ChangeDutyCycle(InvGreen)
    BL.ChangeDutyCycle(InvBlue)

'''
This part of the code pertains to the voice-to-text pipeline at the center of SignScribe
'''
def VoiceToText():
	ExitButtonPressed = False
	
	#the first few lines are initial setup for vosk and pyaudio

	'''
 	a recognizer in vosk terms is the functionality responcible for interpreting the audio into speech.
  	Here a recognizer is being initialized with a model path and the sample rate of the audio to interpret (in Hertz) in this case it's 16 kHz
   	NOTE:
    		-The sample rate must be the same as the sample rate of audio otherwise it may lead to issues in transcription accuracy
      		-Vosk models run best at 16 kHz though other samples rate will be adjusted automatically by vosk
		-Vosk models other than sampling require audio to be inputted with the following configuration:
  			-Mono Channel or 1 channel
     			-Audio format must be in PCM form (often as .WAV or .RAW)
			-Vosk is typically used with 16-bit audio, but it can handle other bit depths if the audio is correctly interpreted and resampled. 
   	You will see this note reflected when initializing the microphone
 	'''
	recognizer = KaldiRecognizer(Model(path), 16000)

	'''
 	Pyaudio is a python wrapper for the open source I/O library, PortAudio
  	A stream is an object that encapsulates PyAudio's functionality, it can be used for various things however here we just use it to read audio
   	This stream automatically connects to the first known audio device on system, if needed set parameter "input_device_index = #"
    	pyaudio.paInt16 - sets bit depth of audio to 16 bits
     	channel = 1 - sets mono audio
      	rate - the sample rate of the audio (MUST BE THE SAME VALUE AS SET IN RECOGNIZER)
        input - boolean that sets whether or not the stream will listen through mic
	frames_per_buffer - The number of frames per buffer. This controls how many audio samples are processed at a time. 
 		Smaller buffer sizes reduce latency but increase CPU usage.
 	'''
	stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
	
        '''
	initiate stream state of listening through mic.
 	'''
	stream.start_stream()
	
	print("Say exit when you want to terminate the program... \n")

	'''
	RGB LED set to green
        '''
	SetRGBColor(0, 100, 0)

	'''
	loop that reads audio input and transcripts it
 	'''
	while True:
		
		'''
		data holds the raw audio input from mic.
  		'''
		data = stream.read(16000)

		'''
  		Optional code for implementing button that stops mechanical hand and saves transcript.
		'''
		'''
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
		'''
		
		'''
		clears cross communication file from previous use
		'''
		with open(file2, 'w') as file:
			pass

		'''
		loop responsible for transcribing raw audio into text
  		'''
		if recognizer.AcceptWaveform(data) == True:

			'''
			result captures recognizer's raw transcription from recognizer.AcceptWaveform method call
   			'''
			result = recognizer.Result()

			'''
   			The raw output of vosk is a json format with a single "text" key
			result_dict translate that raw JSON data into a dictionary 
   			'''
			result_dict = json.loads(result)

			'''
			translates the previouse dictionary into pure string text of words 
   			'''
			text = result_dict.get("text","")

			'''
			formats string of words into a list of words
   			'''
			newText = text.split()

			'''
			stores newly inputed text into wordBackLog and fullTranscript
   			'''
			for i in newText:
				if i not in censorFilter:
					if i != "huh":
						wordBacklog.append(i)
						fullTranscript.append(i)
				else:
					wordBacklog.append("[censored]")
					fullTranscript.append("[censored]")
				'''
				communicates to the GUI the current contents of wordBacklog for real time display
    				'''
				GUI_text_queue.put(' '.join(wordBacklog))

			'''
			outputs word backlog (for debugging purposes)
   			'''
			if not wordBacklog == []:
				print(str(wordBacklog))
				
			'''
			quits program if exit word has been stated & if autosave is True, appends full transcript to a file
   			'''
				if exitWord in text.lower() or ExitButtonPressed == True:
					print("Exiting...\n")
					print("AUTOSAVE IS: ",autoSave)
					if autoSave == True:
						with open(file2, 'a') as f2:
							f2.write(str(fullTranscript) + '\n')
						print("Contents of text transcript have been automatically saved to ", file2)
						
					'''
					Stops data collection
     					'''
					SetRGBColor(100, 0, 0)

					'''
					Ends stream reading state
     					'''
					stream.stop_stream()
					stream.close()
					sleep(2)
					SetRGBColor(0, 0, 0)
					exit()

'''
This function encapsulates the central control flow process of our hand and GUI.
It takes in wordBacklog and iterates through each letter to be signed by the robotic hand
'''
def letterSwitch():

	'''
	stop -  translates the raw string of user-defined exitWord into a detectable list
	when this list is detected in wordBacklog the program with terminate 
        '''
	stop = exitWord.split();
	
	'''
	main loop that process through the wordBacklog
 	'''
	while True:
		
		'''
		checks if the exitWord has been spoken, if it has the hand will not sign it
  		'''
		if not wordBacklog == [] and not set(stop).issubset(set(wordBacklog)) and wordBacklog[0] != "[censored]" and wordBacklog[0] != "huh":

			'''
			disect wordbacklog into letters & run appropriate function
   			'''
			for letter in wordBacklog[0]:
				
				'''
				main switch statement that has the robotics hand sign each letter 
    				'''
				match letter:

					'''
					example: when a is detected in wordBacklog[0] (first word in wordBacklog at the moment)
     					'''
					case 'a':

						'''
						controlServo is called and each motor is set to these specific position to emulate the equivalent motion/pose expected in ASL
      						'''
						controlServo(serv1 = 100, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 135)

						'''
						GUI_hand_queue captures the current letter in process and sends it to the GUI thread for animating
      						'''
						GUI_hand_queue.put('a')

						'''
						after each pose the hand waits lettersPause amount of seconds before moving on
      						'''
						sleep(lettersPause)
						
					case 'b':
						controlServo(serv1 = 10, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10, serv6 = 90, serv7 = 90)
						GUI_hand_queue.put('b')
						sleep(lettersPause)
						
					case 'c':
						controlServo(serv1 = 80, serv2 = 90, serv3 = 90, serv4 = 90, serv5 = 90, serv6 = 180, serv7 = 90)
						GUI_hand_queue.put('c')
						sleep(lettersPause)
						
					case 'd':
						controlServo(serv1 = 10, serv2 = 10, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 180, serv7 = 90)
						GUI_hand_queue.put('d')
						sleep(lettersPause)
						
					case 'e':
						controlServo(serv1 = 50, serv2 = 110, serv3 = 115, serv4 = 125, serv5 = 120, serv6 = 90, serv7 = 90)
						GUI_hand_queue.put('e')
						sleep(lettersPause)
						
					case 'f':
						controlServo(serv1 = 10, serv2 = 160, serv3 = 10, serv4 = 10, serv5 = 10, serv6 = 180, serv7 = 90)
						GUI_hand_queue.put('f')
						sleep(lettersPause)
						
					case 'g':
						controlServo(serv1 = 80, serv2 = 40, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 180, serv7 = 135)
						GUI_hand_queue.put('g')
						sleep(lettersPause)
						
					case 'h':
						controlServo(serv1 = 10, serv2 = 40, serv3 = 80, serv4 = 160, serv5 = 160, serv6 = 180, serv7 = 180)
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
						controlServo(serv1 = 20, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 180, serv7 = 90)
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
						controlServo(serv1 = 10, serv2 = 60, serv3 = 40, serv4 = 160, serv5 = 160, serv6 = 180, serv7 = 90)
						GUI_hand_queue.put('r')
						sleep(lettersPause)
						
					case 's':
						controlServo(serv1 = 10, serv2 = 160, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 45)
						GUI_hand_queue.put('s')
						sleep(lettersPause)
						
					case 't':
						controlServo(serv1 = 10, serv2 = 80, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
						GUI_hand_queue.put('t')
						sleep(lettersPause)
						
					case 'u':
						controlServo(serv1 = 60, serv2 = 10, serv3 = 10, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
						GUI_hand_queue.put('u')
						sleep(lettersPause)
						
					case 'v':
						controlServo(serv1 = 10, serv2 = 40, serv3 = 10, serv4 = 160, serv5 = 160, serv6 = 90, serv7 = 90)
						GUI_hand_queue.put('v')
						sleep(lettersPause)
						
					case 'w':
						controlServo(serv1 = 10, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 160, serv6 = 90, serv7 = 90)
						GUI_hand_queue.put('w')
						sleep(lettersPause)
						
					case 'x':
						controlServo(serv1 = 10, serv2 = 80, serv3 = 160, serv4 = 160, serv5 = 160, serv6 = 180, serv7 = 90)
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

			'''
			resets the pose of the hand into a 'default' open palm pose
   			'''
			controlServo(serv1 = 160, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10, serv6 = 90, serv7 = 90)

			'''
			at the end of each letter iteration the loop waits a wordsPause amount of seconds
   			'''
			sleep(wordsPause)

		'''
		Optional code used to censor inappropriate words
		'''
		'''
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
		'''
				
		'''
		checks if wordBacklog is empty
		'''
		if not wordBacklog == []:
				
			'''
			removes words have been fully signed at the end of the iteration
   			'''
			wordBacklog.remove(wordBacklog[0])

'''			
actual running of program starts here
'''
Setup()

SetRGBColor(0, 0, 100)

'''
starts robotic hand off in 'default' open  palm pose
'''
controlServo(serv1 = 160, serv2 = 10, serv3 = 10, serv4 = 10, serv5 = 10, serv6 = 90, serv7 = 90)


'''
Allows hand to move to default position before starting
'''
sleep(2)

'''
initiate and run threading (multiprocessing)
'''

'''
fail safe so that the robotic hand has a minimum of 0.4 seconds in order to play out in a legible pace
'''
if not lettersPause >= 0.4:
	lettersPause = 0.4

'''
GUI_Thread is responsible for everything to do with GUI, if it is disabled then no window will show up on program startup
if the user defined autoLaunch permits the GUI to automatically launch on startup of program then the GUI thread will initiate
'''
if autoLaunch == "True":
	GUI_Thread = thread.Thread(target=InterfaceMain.GUI_APP,args=[GUI_text_queue, wordBacklog, GUI_hand_queue])

'''
ServoThread - it processes the text and translates it into letter posing/motions for the robotic hand and GUI 
ServoThread is initialized
'''
ServoThread = thread.Thread(target=letterSwitch)

'''
VoiceThread is responsible for retrieving audio from the microphone and translating said audio into text 
VoiceThread is initialized
'''
VoiceThread = thread.Thread(target=VoiceToText)
	
'''
if the user defined autoLaunch permits the GUI to automatically launch on startup of program then the GUI thread will start execution
'''
if autoLaunch == "True":
	GUI_Thread.start()

'''
the following threads with commence execution 
'''
ServoThread.start()
VoiceThread.start()

'''
if the user defined autoLaunch permits the GUI to automatically launch on startup of program then the GUI thread will be terminated after execution finishes
'''
if autoLaunch == "True":
	GUI_Thread.join()

'''
the following threads will terminate after execution of the threads are finished 
'''
ServoThread.join()
VoiceThread.join()
