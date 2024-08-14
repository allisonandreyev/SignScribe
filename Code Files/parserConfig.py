'''
Function for reading config file.
'''
def configParser():

    '''
    Specifies file path of config file and sets it to a variable
    '''
    file2 = '/home/signscribe/Downloads/SignScribe-master/Code Files/Config.txt'

    '''
    Config Variables
    '''
    exitWord=None
    wordsPause=None
    lettersPause=None
    autoSave=None
    autoLaunch=None
    censorFilter=[]

    '''
    Opens file as read.
    '''
    with open(file2, 'r') as file:

        '''
        Sorts through each line in config file and updates variables to config data.
        '''
        for line in file:
            
            '''
            Identifies current line.
            '''
            if "exitWord" in line:
                
                '''
                Creates local list that contains inputted value of corresponding line in config file.
                '''
                ls = line.split("\"")

                '''
                Sets unique variable to inputted value of corresponding line in config file.
                '''
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
                censorFilter = ls[1].split()
            elif "autoLaunch" in line:
                ls = line.split("\"")
                autoLaunch = ls[1]

    '''
    Returns all inputted values from config file.
    '''
    return exitWord, wordsPause, lettersPause, autoSave, filter1, autoLaunch

'''
Runs configParser function.
'''
configParser()
