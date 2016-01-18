import SendEmail
from Thermconfig import config

# SMTP credentials
def getAuth():
    with open(config['alerts']['authFile'], 'r') as file:
        return file.read().splitlines()

# Compose everything into the email and send it
def alertMe(subject, body=''):
    auth = getAuth()
    username = auth[0]
    password = auth[1]
    recipient = auth[2]

    sendEmail.sendEmail(username, password, recipient, subject, body)

def thermAlert(pod, softTemps):
    if pod.tooHigh:
        direction = ' too high:'
    else:
        direction = ' too low:'
    subject = pod.label + direction + softTemps['CString'] + softTemps['FString']
    alertMe(subject)
