#!/usr/bin/python3

# Returns the C and F temperatures for configured 1wire themocouples
from configobj import ConfigObj
import os.path

whereAmI = os.path.dirname(os.path.abspath(__file__)) + '/'
config = ConfigObj(whereAmI + 'thermostasis.conf')

Thermocouples = config['thermocouples']

class Temp:
    def getTemp(self):
        # Open a 1wire device, get the relevant data
        path = '/sys/bus/w1/devices/' + self.vals['serial'] + '/w1_slave'
        with open(path, 'r') as thermFile:
            tempLine = thermFile.read().splitlines()[1]
            temp = int(tempLine.split('t=')[-1])
        # Convert millidegrees C to usable numbers
        self.CTemp = temp / 1000
        self.FTemp = self.CTemp * 1.8 + 32
        # Prep some soft strings for meatbags
        self.CString = str(self.CTemp)[:7] + 'C'
        self.FString = str(self.FTemp)[:7] + 'F'
    
    def checkTolerance(self, tolerance):
        # Check if the temp is in acceptable range
        # Returns true if there isn't a defined target and tolerance
        try:
            target = self.vals['target']
            self.inTolerance = False
            if self.CTemp > target + tolerance:
                self.direction = 'too high'
            elif self.CTemp < target - tolerance:
                self.direction = 'too low'
            else:
                self.inTolerance = True
        except KeyError:
            # if there isn't a defined target
            self.inTolerance = True
    
    def heat():
        try:
            setPowerState(self.vals['heatPin'], True)
        except KeyError:
            pass
        try:
            setPowerState(self.vals['coolPin'], False)
        except KeyError:
            pass
    def cool()
        try:
            setPowerState(self.vals['coolPin'], True)
        except KeyError:
            pass
        try:
            setPowerState(self.vals['heatPin'], False)
        except KeyError:
            pass

    def maintainTemp(self, temp, tolerance):
        try:
            self.checkTolerance(self.vals['tolerance'])
            if not self.inTolerance:
                if self.direction == 'too high':
                    self.cool()
                else:
                    self.heat()
        except KeyError:
            # means that the tolerance wasn't defined
            pass
        try:
            self.checkTolerance(self.vals['alertTolerance'])
            if not self.inTolerance:
                alertString = label + ' ' + self.direction + ': ' +
                            self.CString + ' ' + self.FString
                alertMe(alertString)
        except KeyError:
            # means that an alertTolerance wasn't defined
            pass

    def __init__(self, label, vals):
        self.label = label
        self.vals = vals
        self.getTemp()

class Pod:
    def __init__(self, label):
        # get the configuration from the config file
        vals = config['pods'][label]
        self.sensor = vals['sensor']
        self.tolerance = vals['tolerance']
        self.alertTolerance = vals['alertTolerance']
        self.heatPin = vals['heatPin']
        self.coolPin = vals['coolPin']

    def checkTemp(self): 
        # get the current temperature
        self.thermometer = Temp(self.sensor)
        return self.thermometer.CTemp

    def checkTolerance():
        


def getAllTemps():
    temps = {}
    for label, vals in Thermocouples.items():
        temp = Temp(label, vals)
        temps[label] = temp
    return temps

# always populate the temps
temps = getAllTemps()
if __name__ == '__main__':
    for label, temp in temps:
        print(label + ' is at ' + temp.CString + ', and ' + 
                                        temp.FString) 
