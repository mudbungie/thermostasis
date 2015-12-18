import RPi.GPIO as GPIO
import time

# turn a pin on or off
def setPowerState(pin, state):
    GPIO.setmode(GPIO.BCM)
    # too much whining
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, state)

# get the temperature from a GPIO-connected thermometer
def readTemp(serialNumber):
    # location of the virtual file that contains the output
    devicePath = '/sys/bus/w1/devices/' + serialNumber +  '/w1_slave'
    # get the temp from the virtual file
    with open(devicePath, 'r') as thermOutput:
        tempLine = thermOutput.read().splitlines()[1]
        temp = int(tempLine.split('t=')[-1])
    return temp

# shoot for a temperature in millidegrees C, assuming a heater is connected
def thermostatic(target, tolerance, heatPin, coolPin, serialNumber):
    currentTemp = readTemp(serialNumber)
    # if it is too cool, turn on the heater
    if currentTemp < (target - tolerance):
        setPowerState(heatPin, True)
        setPowerState(coolPin, False)
    # if it is too hot, turn on the cooler
    elif currentTemp > (target - tolerance):
        setPowerState(heatPin, False)
        setPowerState(coolPin, True)

if __name__ == '__main__':
    myTarget = 21111
    myTolerance = 1000
    myHeatPin = 15
    myCoolPin = 23 # I don't presently have a cooler connected
    mySerialNumber = '28-0000075d0acc'
    while True:
        thermostatic(myTarget, myTolerance, myHeatPin, myCoolPin, mySerialNumber)
        time.sleep(1)
