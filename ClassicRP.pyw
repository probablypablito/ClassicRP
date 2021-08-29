from pypresence import Presence
import time
import psutil
import os.path
import subprocess
from subprocess import Popen
client_id = "799077669294702595"
RPC = Presence(client_id)  # Initialize the Presence client
RPC.connect() # Start the handshake loop

savedLevel = 0
currentLevel = 0
currentDeaths = 0
savedDeaths = 0
currentBerries = 0
savedBerries = 0
rpcInfo = dict()
p8Location = ""

def checkIfProcessRunning(processName): # Check if process is running. Stolen from https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def checkLevel():
    global savedLevel, currentLevel
    leveltxt = open('level.txt', "r")
    currentLevel = leveltxt.readline().strip()
    leveltxt.close()
    
    if (savedLevel != currentLevel):
        savedLevel = currentLevel
        if (savedLevel == "0"):
            rpcInfo['details'] = "Main Menu"
            rpcInfo['small_image'] = "nothing"
        elif (savedLevel == "12"):
            rpcInfo['details'] = "Old Site"
        elif (savedLevel == "23"):
            dashestxt = open('dashes.txt', "r")
            if (dashestxt.read(1) == "1"):
                rpcInfo['small_image'] = "gemskip"
                rpcInfo['small_text'] = "Gemskip"
            else:
               rpcInfo['small_image'] = "gem"
               rpcInfo['small_text'] = "Normal"
            rpcInfo['details'] = savedLevel + "00m"
            dashestxt.close()
        elif (savedLevel == "31"):
            rpcInfo['details'] = "Summit"
        else:
            rpcInfo['details'] = savedLevel + "00m"
        rpcInfo['large_image'] = savedLevel + "00m"

def checkOther():
    global savedDeaths, currentDeaths, savedBerries, currentBerries
    deathtxt = open('deaths.txt', "r")
    currentDeaths = deathtxt.readline().strip()
    deathtxt.close()
    
    berrytxt = open('berries.txt', "r")
    currentBerries = berrytxt.readline().strip()
    berrytxt.close()
    
    if (savedDeaths != currentDeaths or savedBerries != currentBerries):
        savedDeaths = currentDeaths
        savedBerries = currentBerries
        rpcInfo['state'] = savedDeaths + "x 💀 | " + str(savedBerries) + "x 🍓"

if (os.path.isfile('./p8path.txt') == False):
    import easygui
    p8Location = easygui.fileopenbox()
    f = open("p8path.txt", "w")
    f.write(p8Location)
    f.close()

else:
    f = open("p8path.txt", "r")
    p8Location = f.readline().strip()
    f.close()

p = Popen([p8Location])

while (checkIfProcessRunning('pico8') == True):    
    checkLevel() # Checks current level and sets the details and image used in the Rich Presence
    checkOther() # Checks current amount of deaths and sets the state to be that
    RPC.update(**rpcInfo) # Update Rich Presence
    print(rpcInfo)
    time.sleep(0.066) # Celeste runs at 30 FPS, but this updates 15 times a second to reduce load 
