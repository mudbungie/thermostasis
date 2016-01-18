import AlertMe
import psutil

# just throw a heads up in case the main thread crashes

def isSystemRunning(cmdString):
    theSystemIsRunning = False

    for process in psutil.process_iter():
        if cmdString in process.cmdline():
            theSystemIsRunning = True

    return theSystemIsRunning

if __name__ == '__main__': 
    cmdString = '/home/pi/thermostasis/Thermostasis.py'
    if not isSystemRunning(cmdString):
        AlertMe.alertMe('Thermostasis isn\'t running')
