import AlertMe
import  

def isSystemRunning(cmdString):
    theSystemIsRunning = False

    for process in psutil.process_iter():
        if cmdString in process.cmdline():
            theSystemIsRunning = True

    return theSystemIsRunning

def checkThings(cmdString):
    systemOnline = isSystemRunning(cmdString)
    if systemOnline == False:
        alertMe('the system isn\'t running')

if __name__ == '__main__': 
    cmdString = 'python3 /home/pi/thermostasis/Thermostasis.py'
    if not isSystemRunning(cmdString):
        AlertMe.alertMe('Thermostasis isn\'t running')
