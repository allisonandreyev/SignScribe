def configParser():
    file2 = 'Config.txt'

    # Config Variables
    exitWord=None
    wordsPause=None
    lettersPause=None
    autoSave=None

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
                exit
    
    return exitWord, wordsPause, lettersPause, autoSave
