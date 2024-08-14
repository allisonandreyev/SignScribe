'''
Function for reading config file.
'''
def configParser():
    file2 = '/home/signscribe/Downloads/SignScribe-master/Code Files/Config.txt'

    # Config Variables
    exitWord=None
    wordsPause=None
    lettersPause=None
    autoSave=None
    autoLaunch=None
    filter1=[]
    
    with open(file2, 'r') as file:
        for line in file:
            if "exitWord" in line:
                ls = line.split("\"")
                exitWord = ls[1]
            elif "wordsPause" in line:
                ls = line.split("\"")
                wordsPause = float(ls[1])
            elif "lettersPause" in line:
                ls = line.split("\"")
                lettersPause = float(ls[1])
            elif "autoSave" in line:
                ls = line.split("\"")
                autoSave = ls[1]
            elif "Words to censor" in line:
                ls = line.split("\"")
                filter1 = ls[1].split()
            elif "autoLaunch" in line:
                ls = line.split("\"")
                autoLaunch = ls[1]
    return exitWord, wordsPause, lettersPause, autoSave, filter1, autoLaunch
    
configParser()
