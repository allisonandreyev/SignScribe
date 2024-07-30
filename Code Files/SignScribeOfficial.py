from vosk import Model, KaldiRecognizer
from time import sleep
import pyaudio
import json
import thread
import RPi.GPIO
import parserConfig
from HandControl import controlServo

#grabs info from config file
exitWord, wordsPause, lettersPause, autoSave, filter = parserConfig.configParser()

wordBacklog = []
fullTranscript = []

file2 = 'fullTranscript.txt'
file1 = 'CrossCommunication.txt'

#vosk model
path=r'/home/signscribe/Downloads/SignScribe-master/Organization/VoskModels/vosk-model-small-en-us-0.15'

def VoiceToText():
	recognizer = KaldiRecognizer(Model(path), 16000)

	stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

	stream.start_stream()
	
	print("Say exit when you want to terminate the program... \n")

	#reads data
	while True:
		data = stream.read(16000)

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
				if i not in filter:
					wordBacklog.append(i)
					fullTranscript.append(i)
				else:
					wordBacklog.append("[censored]")
					fullTranscript.append("[censored]")

			#outputs word backlog (for debugging purposes)
			if not wordBacklog == []:
				print(str(wordBacklog))
			#appends cross communication.txt
			with open(file1, 'a') as f:
				f.write(str(wordBacklog) + '\n')

			#quits program if exit word has been stated & if autosave is True, appends full transcript to a file
			if exitWord in text.lower():
				print("Exiting...\n")
				print("AUTOSAVE IS: ",autoSave)
				if autoSave == True:
					with open(file2, 'a') as f2:
						f2.write(str(fullTranscript) + '\n')
					print("Contents of text transcript have been automatically saved to ", file2)
					
				
				# stops data collection
				stream.stop_stream()
				stream.close()
				exit


def letterSwitch():
	sleep(2)
	
	stop = exitWord.split();
	
	while True:
		
		sleep(wordsPause)

		#checks if the exit word has been spoken, if it has the hand will not sign it
		if not wordBacklog == [] and not set(stop).issubset(set(wordBacklog)) and wordBacklog[0] is not "[censored]":
			for letter in wordBacklog[0]: 
				sleep(lettersPause)
				
				#disect word back log into letters & run appropriate function
				match letter:
					case 'a':
						controlServo(80, 160, 160, 160, 160)
					case 'b':
						controlServo(10,10,10,10,10)
					case 'c':
						controlServo(80, 80, 80, 80, 80)
					case 'd':
						controlServo(10, 160, 160, 160, 10)
					case 'e':
						controlServo(10, 160, 160, 160, 160)
					case 'f':
						controlServo(10, 160, 10, 10, 10)
					case 'g':
						controlServo(80, 10, 160, 160, 160)
					case 'h':
						controlServo(40, 160, 160, 160, 160)
					case 'i':
						controlServo(10, 160, 160, 160, 10)
					case 'j':
						controlServo(10, 160, 160, 160, 10)
						sleep(lettersPause)
						controlServo(10, 160, 160, 160, 160)
						sleep(lettersPause)
						controlServo(10, 160, 160, 160, 10)
					case 'k':
						controlServo(160, 10, 10, 160, 160)
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
						sleep(lettersPause)
						controlServo(160, 160, 160, 160, 160)
						sleep(lettersPause)
						controlServo(10, 160, 160, 160, 160)
					case 't':
						controlServo(10, 80, 60, 160, 160)
					case 'u':
						controlServo(60, 10, 10, 160, 160)
					case 'v':
						controlServo(10, 10, 10, 160, 160)
						sleep(lettersPause)
						controlServo(10, 160, 160, 160, 160)
						sleep(lettersPause)
						controlServo(10, 10, 10, 160, 160)
					case 'w':
						controlServo(10, 10, 10, 10, 160)
					case 'x':
						controlServo(10, 40, 160, 160, 160)
					case 'y':
						controlServo(160, 160, 160, 160, 10)
					case 'z':
						controlServo(10, 10, 160, 160, 160)
			print(" ")
			controlServo(160, 10, 10, 10, 10)
			sleep(lettersPause)
				
			#update wordbacklog to remove what the hand already signed
			wordBacklog.remove(wordBacklog[0])

#reset to default position
sleep(2)
controlServo(160, 10, 10, 10, 10)
sleep(4)

#initiate and run threading (multiprocessing)
ServoThread = thread.Thread(target=letterSwitch)
VoiceThread = thread.Thread(target=VoiceToText)

ServoThread.start()
VoiceThread.start()

ServoThread.join()
VoiceThread.join()
