# To send emails if things are wrong

import sendEmail
import psutil
import os
import reportTemp

# SMTP credentials
def getAuth():
    sourceLoc = os.path.dirname(os.path.abspath(__file__)) + '/'
    with open(sourceLoc + 'auth', 'r') as file:
        return file.read().splitlines()

# Compose everything into the email and send it
def alertMe(subject, body):
    auth = getAuth()
    username = auth[0]
    password = auth[1]
    recipient = auth[2]

    sendEmail.sendEmail(username, password, recipient, subject, body)

def checkTemp(target, tolerance, scale='C'):
    thermostats = reportTemp.reportAllTemps()

    inTolerance = False

    for label, temps in thermostats.items():
        if temps[scale] > target + tolerance:
            direction = 'too high'
        elif temps[scale] < target - tolerance:
            direction = 'too low'
        else:
            inTolerance = True
            direction = 'in tolerance'
        if not inTolerance:
            alertMe(label + ' temp ' + direction + ': ' + str(temps['C'])[:7] + 'C ' + 
                                    str(temps['F'])[:7] + 'F', '')

def isSystemRunning(cmdString):
    theSystemIsRunning = False

    for process in psutil.process_iter():
        if cmdString in process.cmdline():
            theSystemIsRunning = True

    return theSystemIsRunning

def checkThings(cmdString, target, tolerance):
    systemOnline = isSystemRunning(cmdString)
    if systemOnline == False:
        alertMe("the system isn't running", '')
    checkTemp(target, tolerance)

if __name__ == '__main__': 
    cmdString = 'python3 /home/pi/thermostasis/thermostasis.py'
    # units in millidegress C
    target = 23.889
    tolerance = 2

    checkThings(cmdString, target, tolerance)
