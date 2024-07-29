from vosk import Model, KaldiRecognizer
from time import sleep
import pyaudio
import json
import thread
import RPi.GPIO
import parserConfig
from HandControl import controlServo

exitWord, wordsPause, lettersPause, autoSave = parserConfig.configParser()

wordBacklog = []
fullTranscript = []

file2 = 'newfilename.txt'
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
				fullTranscript.append(i)
			
			if not wordBacklog == []:
				print(str(wordBacklog))
			
			with open(file1, 'a') as f:
				f.write(str(wordBacklog) + '\n')
		
			if exitWord in text.lower():
				print("Exiting...\n")
				print("AUTOSAVE IS: ",autoSave)
				if autoSave == True:
					with open(file2, 'a') as f2:
						f2.write(str(fullTranscript) + '\n')
					print("Contents of text transcript have been automatically saved to ", file2)
					
				
				# use 'pass' to be able to clear file after other program ran
				stream.stop_stream()
				stream.close()
				exit


def letterSwitch():
	sleep(2)
	stop = exitWord.split();
	while True:
		sleep(wordsPause)
		if not wordBacklog == [] and not set(stop).issubset(set(wordBacklog)):
			for letter in wordBacklog[0]: 
				sleep(lettersPause)
				#disect first word into letters
				match letter:
					case 'a':
						controlServo(80, 160, 160, 160, 160)
						print("a")
					case 'b':
						controlServo(0, 0, 0, 0, 0)
						print("b")
					case 'c':
						controlServo(80, 80, 80, 80, 80)
						print("c")
					case 'd':
						controlServo(0, 160, 160, 160, 0)
						print("d")
					case 'e':
						controlServo(0, 160, 160, 160, 160)
						print("e")
					case 'f':
						controlServo(0, 160, 0, 0, 0)
						print("f")
					case 'g':
						controlServo(80, 0, 160, 160, 160)
						print("g")
					case 'h':
						controlServo(40, 160, 160, 160, 160)
						print("h")
					case 'i':
						controlServo(0, 160, 160, 160, 0)
						print("i")
					case 'j':
						controlServo(0, 160, 160, 160, 0)
						sleep(lettersPause)
						controlServo(0, 160, 160, 160, 160)
						sleep(lettersPause)
						controlServo(0, 160, 160, 160, 0)
						print("j")
					case 'k':
						controlServo(160, 0, 0, 160, 160)
						print("k")
					case 'l':
						controlServo(160, 0, 160, 160, 160)
						print("l")
					case 'm':
						controlServo(0, 80, 80, 80, 160)
						print("m")
					case 'n':
						controlServo(0, 80, 80, 160, 160)
						print("n")
					case 'o':
						controlServo(0, 160, 160, 160, 160)
						print("o")
					case 'p':
						controlServo(80, 0, 100, 160, 160)
						print("p")
					case 'q':
						controlServo(80, 80, 160, 160, 160)
						print("q")
					case 'r':
						controlServo(0, 40, 40, 160, 160)
						print("r")
					case 's':
						controlServo(0, 160, 160, 160, 160)
						sleep(lettersPause)
						controlServo(160, 160, 160, 160, 160)
						sleep(lettersPause)
						controlServo(0, 160, 160, 160, 160)
						print("s")
					case 't':
						controlServo(0, 80, 60, 160, 160)
						print("t")
					case 'u':
						controlServo(60, 0, 0, 160, 160)
						print("u")
					case 'v':
						controlServo(0, 0, 0, 160, 160)
						sleep(lettersPause)
						controlServo(0, 160, 160, 160, 160)
						sleep(lettersPause)
						controlServo(0, 0, 0, 160, 160)
						print("v")
					case 'w':
						controlServo(0, 0, 0, 0, 160)
						print("w")
					case 'x':
						controlServo(0, 40, 160, 160, 160)
						print("x")
					case 'y':
						controlServo(160, 160, 160, 160, 0)
						print("y")
					case 'z':
						controlServo(0, 0, 160, 160, 160)
						print("z")
					case _:
						print("'")
			print(" ")
			controlServo(160, 0, 0, 0, 0)
			sleep(lettersPause)
				
			#deprecate the same first workword here
			wordBacklog.remove(wordBacklog[0])

sleep(2)
controlServo(160, 0, 0, 0, 0)
sleep(4)
ServoThread = thread.Thread(target=letterSwitch)
VoiceThread = thread.Thread(target=VoiceToText)

ServoThread.start()
VoiceThread.start()

ServoThread.join()
VoiceThread.join()
