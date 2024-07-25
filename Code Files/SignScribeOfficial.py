from vosk import Model, KaldiRecognizer
from time import sleep
import pyaudio
import json
import thread
import RPi.GPIO

RPi.GPIO.setwarnings(False)
RPi.GPIO.setmode(RPi.GPIO.BOARD)
RPi.GPIO.setup(37, RPi.GPIO.OUT)
Servo1PWM = RPi.GPIO.PWM(37, 50)
Servo1PWM.start(0)
wordBacklog = []

file1 = 'CrossCommunication.txt'

print("What model would you like?\n")
print("1. Super small")
print("2. Small")
print("3. Medium")
userChoice = int(input("Selection (1-3) : "))

if userChoice == 2:
	path=r'/home/signscribe/Downloads/SignScribe-master/Organization/VoskModels/vosk-model-en-us-0.22-lgraph'
elif userChoice == 3:
	path=r'/home/signscribe/Downloads/SignScribe-master/Organization/VoskModels/vosk-model-en-us-0.22'
else:
	path=r'/home/signscribe/Downloads/SignScribe-master/Organization/VoskModels/vosk-model-small-en-us-0.15'

def ServoMove():
	InputAngle = 180
	while True:
		sleep(2)
		if InputAngle == 180:
			InputAngle = 0
		else:
			InputAngle = 180
		ServoDuty = InputAngle / 18 + 2.5
		RPi.GPIO.output(37, True)
		Servo1PWM.ChangeDutyCycle(ServoDuty)
		sleep(1)
		RPi.GPIO.output(37, False)
		Servo1PWM.ChangeDutyCycle(0)

def VoiceToText():
	recognizer = KaldiRecognizer(Model(path), 16000)

	stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

	stream.start_stream()
	
	print("Say exit when you want to terminate the program... \n")
	
	while True:
		data = stream.read(16000)
		
		with open(file1, 'w') as file:
			pass
	
		if recognizer.AcceptWaveform(data) == True:
			result = recognizer.Result()
			result_dict = json.loads(result)
			text = result_dict.get("text","")
			newText = text.split()
			for i in newText:
				wordBacklog.append(i)
			
			if not wordBacklog == []:
				print(str(wordBacklog))
			
			with open(file1, 'a') as f:
				f.write(str(wordBacklog) + '\n')
		
			if "stop sign scribe" in text.lower():
				print("Exiting...\n")
				#call other file to move hand
				print("File with speech transcription will now be cleared for the next session.")
				print("Enter '1' if you have transfered the contents of the file and/or want it to be cleared: ")
				choice = int(input())
				if choice == 1:
					with open(file1, 'w') as file:
						pass
				print("File contents of '" + file1 + "' have been cleared.")
				break
				
	# use 'pass' to be able to clear file after other program ran
	stream.stop_stream()
	stream.close()


def letterSwitch():
	sleep(2)
	stop = ["stop","sign", "scribe"]
	while True:
		sleep(0.05)
		if not wordBacklog == [] and not set(stop).issubset(set(wordBacklog)):
			for letter in wordBacklog[0]: 
				#disect first word into letters
				match letter:
					case 'a':
						#smth
						print("a")
					case 'b':
						#smth
						print("b")
					case 'c':
						print("c")
					case 'd':
						print("d")
					case 'e':
						#smth
						print("e")
					case 'f':
						#smth
						print("f")
					case 'g':
						#smth
						print("g")
					case 'h':
						#smth
						print("h")
					case 'i':
						#smth
						print("i")
					case 'j':
						#smth
						print("j")
					case 'k':
						#smth
						print("k")
					case 'l':
						#smth
						print("l")
					case 'm':
						#smth
						print("m")
					case 'n':
						#smth
						print("n")
					case 'o':
						#smth
						print("o")
					case 'p':
						#smth
						print("p")
					case 'q':
						#smth
						print("q")
					case 'r':
						#smth
						print("r")
					case 's':
						#smth
						print("s")
					case 't':
						#smth
						print("t")
					case 'u':
						#smth
						print("u")
					case 'v':
						#smth
						print("v")
					case 'w':
						#smth
						print("w")
					case 'x':
						#smth
						print("x")
					case 'y':
						#smth
						print("y")
					case 'z':
						#smth
						print("z")
					case _:
						#smth
						print("'")
			print(" ")
				
			#deprecate the same first workword here
			wordBacklog.remove(wordBacklog[0])
	
ServoThread = thread.Thread(target=letterSwitch)
VoiceThread = thread.Thread(target=VoiceToText)

ServoThread.start()
VoiceThread.start()

ServoThread.join()
VoiceThread.join()
