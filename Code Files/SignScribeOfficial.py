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

#grabs info from config file
exitWord, wordsPause, lettersPause, autoSave, filter1 = parserConfig.configParser()

wordBacklog = ["abcdefghijklmnopqrstuvwxyz"]
fullTranscript = []

GUI_text_queue = queue.Queue()
GUI_hand_queue = queue.Queue()

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
		if not wordBacklog == [] and not set(stop).issubset(set(wordBacklog)) and wordBacklog[0] != "[censored]":
			for letter in wordBacklog[0]: 
				sleep(lettersPause)
				
				#disect word back log into letters & run appropriate function
				match letter:
					case 'a':
						controlServo(80, 160, 160, 160, 160)
						GUI_hand_queue.put('a')
					case 'b':
						controlServo(10,10,10,10,10)
						GUI_hand_queue.put('b')
					case 'c':
						controlServo(80, 80, 80, 80, 80)
						GUI_hand_queue.put('c')
					case 'd':
						controlServo(10, 160, 160, 160, 10)
						GUI_hand_queue.put('d')
					case 'e':
						controlServo(10, 160, 160, 160, 160)
						GUI_hand_queue.put('e')
					case 'f':
						controlServo(10, 160, 10, 10, 10)
						GUI_hand_queue.put('f')
					case 'g':
						controlServo(80, 10, 160, 160, 160)
						GUI_hand_queue.put('g')
					case 'h':
						controlServo(40, 160, 160, 160, 160)
						GUI_hand_queue.put('h')
					case 'i':
						controlServo(10, 160, 160, 160, 10)
						GUI_hand_queue.put('i')
					case 'j':
						controlServo(10, 160, 160, 160, 10)
						sleep(lettersPause)
						controlServo(10, 160, 160, 160, 160)
						sleep(lettersPause)
						controlServo(10, 160, 160, 160, 10)
						GUI_hand_queue.put('j')
					case 'k':
						controlServo(160, 10, 10, 160, 160)
						GUI_hand_queue.put('k')
					case 'l':
						controlServo(160, 10, 160, 160, 160)
						GUI_hand_queue.put('l')
					case 'm':
						controlServo(10, 80, 80, 80, 160)
						GUI_hand_queue.put('m')
					case 'n':
						controlServo(10, 80, 80, 160, 160)
						GUI_hand_queue.put('n')
					case 'o':
						controlServo(10, 160, 160, 160, 160)
						GUI_hand_queue.put('o')
					case 'p':
						controlServo(80, 10, 100, 160, 160)
						GUI_hand_queue.put('p')
					case 'q':
						controlServo(80, 80, 160, 160, 160)
						GUI_hand_queue.put('q')
					case 'r':
						controlServo(10, 40, 40, 160, 160)
						GUI_hand_queue.put('r')
					case 's':
						controlServo(10, 160, 160, 160, 160)
						sleep(lettersPause)
						controlServo(160, 160, 160, 160, 160)
						sleep(lettersPause)
						controlServo(10, 160, 160, 160, 160)
						GUI_hand_queue.put('s')
					case 't':
						controlServo(10, 80, 60, 160, 160)
						GUI_hand_queue.put('t')
					case 'u':
						controlServo(60, 10, 10, 160, 160)
						GUI_hand_queue.put('u')
					case 'v':
						controlServo(10, 10, 10, 160, 160)
						sleep(lettersPause)
						controlServo(10, 160, 160, 160, 160)
						sleep(lettersPause)
						controlServo(10, 10, 10, 160, 160)
						GUI_hand_queue.put('v')
					case 'w':
						controlServo(10, 10, 10, 10, 160)
						GUI_hand_queue.put('w')
					case 'x':
						controlServo(10, 40, 160, 160, 160)
						GUI_hand_queue.put('x')
					case 'y':
						controlServo(160, 160, 160, 160, 10)
						GUI_hand_queue.put('y')
					case 'z':
						controlServo(10, 10, 160, 160, 160)
						GUI_hand_queue.put('z')
			print(" ")
			controlServo(160, 10, 10, 10, 10)
			sleep(lettersPause)
		elif not wordBacklog == [] and wordBacklog[0] == "[censored]":
			controlServo(160, 10, 10, 10, 10)
			sleep(0.2)
			controlServo(10, 160, 160, 160, 160)
			sleep(0.2)
			controlServo(160, 10, 10, 10, 10)			
			sleep(0.2)
			controlServo(10, 160, 160, 160, 160)
			sleep(0.2)
			controlServo(160, 10, 10, 10, 10)	
		if not wordBacklog == []:
			wordBacklog.remove(wordBacklog[0])
			
#reset to default position
sleep(2)
controlServo(160, 10, 10, 10, 10)
sleep(4)

#initiate and run threading (multiprocessing)
#GUI_Thread = thread.Thread(target=UI_Stuff.GUI_APP,args=[GUI_text_queue, wordBacklog, GUI_hand_queue])
ServoThread = thread.Thread(target=letterSwitch)
VoiceThread = thread.Thread(target=VoiceToText)

#GUI_Thread.start()
ServoThread.start()
VoiceThread.start()

#GUI_Thread.join()
ServoThread.join()
VoiceThread.join()
