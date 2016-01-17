#!/usr/bin/python3

# Returns the C and F temperatures for configured 1wire themocouples
from configobj import ConfigObj
import os.path

whereAmI = os.path.dirname(os.path.abspath(__file__)) + '/'
config = ConfigObj(whereAmI + 'thermostasis.conf')

Thermocouples = config['thermocouples']

class Temp:
    def __init__(self, serial, target=None, tolerance=None):
        # Open a 1wire device, get the relevant data
        path = '/sys/bus/w1/devices/' + serial + '/w1_slave'
        with open(path, 'r') as thermFile:
            tempLine = thermFile.read().splitlines()[1]
            temp = int(tempLine.split('t=')[-1])
        # Convert millidegrees C to usable numbers
        self.CTemp = temp / 1000
        self.FTemp = self.CTemp * 1.8 + 32
        # Prep some soft strings for meatbags
        self.CString = str(self.CTemp)[:7] + 'C'
        self.FString = str(self.FTemp)[:7] + 'F'

        # Check if everything is in acceptable range
        if target and tolerance:
            self.inTolerance = False
            if self.CTemp > target + tolerance:
                self.direction = 'too high'
            elif self.CTemp < target - tolerance:
                self.direction = 'too low'
            else:
                self.inTolerance = True
        else:
            self.inTolerance = True


def getAllTemps():
    temps = {}
    for label, vals in Thermocouples.items():
        if 'target' in vals and 'tolerance' in vals:
            target = float(vals['target'])
            tolerance = float(vals['tolerance'])
            temp = Temp(vals['serial'], target, tolerance)
        else:
            temp = Temp(vals['serial'])
        temps[label] = temp
    return temps

if __name__ == '__main__':
    for label, temp in getAllTemps().items():
        print(label + ' is at ' + temp.CString + ', and ' + 
                                        temp.FString) 
