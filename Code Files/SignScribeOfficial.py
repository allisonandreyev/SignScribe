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

if userChoice == 1:
	path=r'/home/sarlauyen/Desktop/VOSK Test Stuff/VOSK Modules/vosk-model-small-en-us-0.15'
elif userChoice == 2:
	path=r'/home/sarlauyen/Desktop/VOSK Test Stuff/VOSK Modules/vosk-model-en-us-0.22-lgraph'
elif userChoice == 3:
	path=r'/home/sarlauyen/Desktop/VOSK Test Stuff/VOSK Modules/vosk-model-en-us-0.22'
else:
	print("GIGA IS GONE!!!")
	sleep(10)
	path=r'/home/sarlauyen/Desktop/VOSK Test Stuff/VOSK Modules/vosk-model-small-en-us-0.15'

def ServoMove():
	InputAngle = 90
	while True:
		sleep(2)
		if InputAngle == 90:
			InputAngle = 0
		else:
			InputAngle = 90
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
			print(str(wordBacklog))
			
			with open(file1, 'a') as f:
				f.write(str(wordBacklog) + '\n')
		
			if "exit" in text.lower():
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

ServoThread = thread.Thread(target=ServoMove)
VoiceThread = thread.Thread(target=VoiceToText)

ServoThread.start()
VoiceThread.start()

ServoThread.join()
VoiceThread.join()
