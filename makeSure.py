# to send emails if things are wrong

# my library
import sendEmail

# not my library
import psutil

def getAuth():
    with open('auth', 'r') as file:
        return file.read().splitlines()

def alertMe(subject, body):
    auth = getAuth()
    username = auth[0]
    password = auth[1]
    recipient = auth[2]

    sendEmail.sendEmail(username, password, recipient, subject, body)

def checkTemp(target, tolerance):
    inTolerance = False

    with open('/sys/bus/w1/devices/28-0000075d0acc/w1_slave', 'r') as thermFile:
        tempLine = thermFile.read().splitlines()[1]
        CTemp = int(tempLine.split('t=')[-1])
        FTemp = (CTemp * 1.8) + 32000

    CTempString = str(CTemp)[0:2] + '.' + str(CTemp)[2:5] + 'C '
    FTempString = str(FTemp)[0:2] + '.' + str(FTemp)[2:5] + 'F '
    
    if CTemp > target - tolerance:
        direction = 'too high'
    elif CTemp < target + tolerance:
        direction = 'too low'
    else:
        inTolerance = True
        direction = 'in tolerance'

    data = {'CTemp': CTempString,
            'FTemp': FTempString,
            'inTolerance': inTolerance,
            'direction': direction}
    
    return data

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

    tempData = checkTemp(target, tolerance)
    if not tempData['inTolerance'] == True:
        if tempData['direction'] == 'too high':
            alertMe('Temp too high: ' + tempData['CTemp'] + tempData['FTemp'], '')
        else:
            alertMe('Temp too low: ' + tempData['CTemp'] + tempData['FTemp'], '')

if __name__ == '__main__': 
    cmdString = 'python3 /home/pi/thermostasis/thermostasis.py'
    # units in millidegress C
    target = 23333
    tolerance = 1000

    checkThings(cmdString, target, tolerance)
