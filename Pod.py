from Thermometer import Thermometer
from Thermconfig import config
import RPi.GPIO as GPIO
import AlertMe

class Pod:
    def __init__(self, label):
        # Get the configuration from the config file
        self.vals = config['pods'][label]
        self.label = label

    def checkTemp(self): 
        # Get the current temperature
        self.thermometer = Thermometer(self.vals['sensor'])
        return self.thermometer.getTemp()

    def checkTolerance(self):
        # See if things are in tolerance, return whether or not things are fine
        currentTemp = self.checkTemp()
        try:
            target = self.vals['target']
        except KeyError:
            # No target set; everything is fine
            return True
        
        # check against the tolerance
        try:
            tolerance = self.vals['tolerance']
            if currentTemp > target + tolerance:
                self.inTolerance = False
                self.tooHigh = True
                self.setState('cool')
            elif currentTemp < target - tolerance:
                self.inTolerance = False
                self.tooHigh = False
                self.setState('heat')
            else:
                self.inTolerance = True
        except KeyError:
            # No tolerance set; everything is fine
            self.inTolerance = True
        if self.inTolerance:
            self.setState('neutral')
        
        # check against the alertTolerance
        try:
            alertTolerance = self.vals['alertTolerance']
            if currentTemp > target + alertTolerance:
                self.inAlertTolerance = False
                self.tooHigh = True
            elif currentTemp < target - alertTolerance:
                self.inAlertTolerance = False
                self.tooHigh = False
            else:
                self.inAlertTolerance = True
        except KeyError:
            # No alertTolerance set; everything is fine
            self.inTolerance = True
        if not self.inAlertTolerance:
            softTemps = self.thermometer.getSoftTemps()
            AlertMe.tempAlert(self, softTemps)
        
    def setState(self, state):
        heat = False
        cool = False
        if state == 'heat':
            heat = True
        elif state == 'cool':
            cool = True
        
        # Setup...
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Set the heat pin appropriately
        try:
            heatPin = self.vals['heatPin']
            GPIO.setup(heatPin, GPIO.OUT)
            GPIO.output(heatPin, heat)
        except KeyError:
            # No heatPin set, everything is fine
            pass
        try:
            coolPin = self.vals['coolPin']
            GPIO.setup(coolPin, GPIO.OUT)
            GPIO.output(coolPin, cool)
        except KeyError:
            # No coolPin set, everything is fine
            pass

