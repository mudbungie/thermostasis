# to send emails if things are wrong

import sendEmail
import psutils

def getAuth():
    with open('auth', 'r') as file:
        return file.read().splitlines()

def alertMe(subject, body):
    auth = getAuth()
    username = auth[0]
    password = auth[1]

    sendEmail.sendEmail(username, password, username, subject, body)

def checkTemp(target, tolerance):
    with open('/sys/bus/w1/devices/28-0000075d0acc/w1_slave', 'r') as thermFile:
        tempLine = thermFile.read().splitlines()[1]
        temp = tempLine.split('t=')[-1]

    tempDeg = str(temp)[0-1]
    tempMilli = str(temp)[2-4]
    tempString = tempDeg + '.' + tempMilli
    
    if temp < target - tolerance:
        alertMe('Temp too high: ' + tempString, '')
    elif temp > target + tolerance:
        alertMe('Temp too low: ' + tempString, '')

def isTheSystemEvenRunning(processName):
    theSystemIsRunning = False

    for process in psutil.process_iter():
        if 'thermostasis.py' in process.name():
            theSystemIsRunning = True

    if theSystemIsRunning == False:
        alertMe("thermostasis.py isn't running", '')
