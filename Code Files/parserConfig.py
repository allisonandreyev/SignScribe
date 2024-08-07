def configParser():
    
    #CONFIG FILE PATH, MUST BE CHANGED
    file2 = '/home/signscribe/Downloads/SignScribe-master/Code Files/Config.txt'

    # Config Variables are initialized
    exitWord=None
    wordsPause=None
    lettersPause=None
    autoSave=None
    autoLaunch=None
    filter1=[]

    #opens file as a readable
    with open(file2, 'r') as file:

        #scans for variable names, splits the line into the variable & what is is assigned to in config
        #then sets the initialzied variable at the top to equal what is is assigned to in the config file 
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
