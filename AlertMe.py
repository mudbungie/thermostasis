import SendEmail
from os import path
from Thermconfig import config

# SMTP credentials
def getAuth():
    authFileName = (path.dirname(path.abspath(__file__)) + '/' + 
                                config['alerts']['authFile'])
    with open(authFileName, 'r') as file:
        return file.read().splitlines()

# Compose everything into the email and send it
def alertMe(subject, body=''):
    auth = getAuth()
    username = auth[0]
    password = auth[1]
    recipient = auth[2]

    return SendEmail.sendEmail(username, password, recipient, subject, body)

def thermAlert(pod, softTemps):
    if pod.tooHigh:
        direction = ' too high:'
    else:
        direction = ' too low:'
    subject = (pod.label + direction + softTemps['CString'] + ' ' +
                                            softTemps['FString'])
    return alertMe(subject)
