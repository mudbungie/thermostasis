#!/usr/bin/python3

# Returns the C and F temperatures for configured 1wire themocouples

thermocouples = {
                'Air':'28-0000075c9aff',
                'Brew':'28-0000075d0acc',
                }

def formatTemp(device):
    # Open a 1wire device 
    path = '/sys/bus/w1/devices/' + device + '/w1_slave'
    with open(path, 'r') as thermFile:
        tempLine = thermFile.read().splitlines()[1]
        temp = int(tempLine.split('t=')[-1])

        CTemp = temp / 1000

        FTemp = CTemp * 1.8 + 32
    return {'C':CTemp, 'F':FTemp}

def reportAllTemps(softReturn = False):
    temps = {}
    softString = ''
    for label, serial in thermocouples.items():
        temperatures = formatTemp(serial)
        temps[label] = temperatures       
        if softReturn: 
            CString = str(temperatures[0])[:7]
            FString = str(temperatures[1])[:7]
            print(label + ' is at ' + CString + 
                    'C, and ' + FString + 'F')
    return temps        

if __name__ == '__main__':
    reportAllTemps(softReturn = True)
