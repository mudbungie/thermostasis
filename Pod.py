from Thermometer import Thermometer
from Thermconfig import config
import RPi.GPIO as GPIO
import AlertMe
from datetime import datetime, timedelta

class Pod:
    def __init__(self, label):
        # Get the configuration from the config file
        self.vals = config['pods'][label]
        self.label = label
        # alerts should start out timed out
        self.lastAlerted = datetime.now() - timedelta(weeks=1)

    def checkTemp(self): 
        # Get the current temperature
        self.thermometer = Thermometer(self.vals['sensor'])
        return self.thermometer.getTemp()

    def checkTolerance(self):
        # See if things are in tolerance, return whether or not things are fine
        currentTemp = self.checkTemp()
        try:
            target = float(self.vals['target'])
        except KeyError:
            # No target set; everything is fine
            return True
        
        # Check against the tolerance
        if 'tolerance' in self.vals:
            tolerance = float(self.vals['tolerance'])
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
        else:
        # No tolerance set; everything is fine
            self.inTolerance = True
        if self.inTolerance:
            self.setState('neutral')
        
        # Check against the alertTolerance
        if 'alertTolerance' in self.vals:
            alertTolerance = float(self.vals['alertTolerance'])
            if currentTemp > target + alertTolerance:
                self.inAlertTolerance = False
                self.tooHigh = True
            elif currentTemp < target - alertTolerance:
                self.inAlertTolerance = False
                self.tooHigh = False
            else:
                self.inAlertTolerance = True
        else:
            # No alertTolerance set; everything is fine
            self.inTolerance = True
        if not self.inAlertTolerance:
            # Logic to prevent swamping with alerts
            if 'updatePeriod' in self.vals:
                updatePeriod = int(self.vals['updatePeriod'])
            else:
                # Default to ten minutes
                updatePeriod = 600
            if self.lastAlerted < datetime.now() - timedelta(seconds=updatePeriod):
                # If it's been the updatePeriod, try to alert
                softTemps = self.thermometer.getSoftTemps()
                if AlertMe.thermAlert(self, softTemps):
                    # If it succeeds, reset the clock
                    self.lastAlerted = datetime.now()
        
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
            heatPin = int(self.vals['heatPin'])
            GPIO.setup(heatPin, GPIO.OUT)
            GPIO.output(heatPin, heat)
        except KeyError:
            # No heatPin set, everything is fine
            pass
        try:
            coolPin = int(self.vals['coolPin'])
            GPIO.setup(coolPin, GPIO.OUT)
            GPIO.output(coolPin, cool)
        except KeyError:
            # No coolPin set, everything is fine
            pass

