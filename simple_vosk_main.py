from vosk import Model, KaldiRecognizer
import pyaudio
import json

#load the model
#recognizer is defined by a directory path to a pre-made model for english referenced in the first constructor argument for kaldi recognizer
#the second constructor argument defines the 'frequency' at which the model runs in (look into this later)
recognizer = KaldiRecognizer(Model(r'C:\Users\user\Downloads\simple_vosk\simple_vosk_virtual_enviornment\vosk-model-small-en-us-0.15'), 16000)

#recognize the Microphone

#pyaudio is cross platform library that enables easy interaction with audio I/O for various uses
#real-time event driven entity that captures and processes audio
#the method PyAudio() initializes the class pyaudio
#defines a new state machine for pyaudio to constantly listen in
stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

#audio state-machine real time stuff starts here 
stream.start_stream()

print("Say exit when you want to terminate the program... \n")

#infinite loop that terminates when the word 'exit' is spoken 
while True:
    #data is a bytes type variables that holds read audio samples 4096 bytes big
    data = stream.read(4096)


    if recognizer.AcceptWaveform(data) == True:

        #result is the captured-text raw sample read from before
        result = recognizer.Result()

        #result dict then takes result and takes out the json looking parts of the raw text output and assign it to a single key dictionary
        #formatted {"text": #####}
        result_dict = json.loads(result)

        #extracts actual text from dictionary format
        text = result_dict.get("text", "")
        print(text)

        #if 'exit' is found within a lowercase version of the text output, then while loop terminates
        if "exit" in text.lower():
            print("Exiting...")
            break

stream.stop_stream()
stream.close()
