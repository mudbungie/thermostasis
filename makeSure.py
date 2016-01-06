# To send emails if things are wrong

import sendEmail
import psutil
import os
import Temp

# SMTP credentials
def getAuth():
    with open(Temp.config['alerts']['authFile'], 'r') as file:
        return file.read().splitlines()

# Compose everything into the email and send it
def alertMe(subject, body=''):
    auth = getAuth()
    username = auth[0]
    password = auth[1]
    recipient = auth[2]

    sendEmail.sendEmail(username, password, recipient, subject, body)

def checkTemps():
    temps = Temp.getAllTemps()
    for label, temp in Temp.getAllTemps().items():
        if temp.inTolerance == False:
            alertMe(label + ' ' + temp.direction + ': ' + 
                        temp.CString + ' ' + temp.FString)

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
    checkTemps()

if __name__ == '__main__': 
    cmdString = 'python3 /home/pi/thermostasis/thermostasis.py'
    isSystemRunning(cmdString)
    checkTemps()
