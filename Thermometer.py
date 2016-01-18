from Thermconfig import config

class Thermometer:
    def __init__(self, label):
        serial = config['thermocouples'][label]['serial']
        # compile the virtual file that is used to address the 1wire device
        self.sensorPath = '/sys/bus/w1/devices/' + serial + '/w1_slave'

    def getTemp(self):
        with open(self.sensorPath, 'r') as sensorFile:
            # cut the usable data out of the raw
            tempLine = sensorFile.read().splitlines()[1]
            temp = int(tempLine.split('t=')[-1])
            self.CTemp = temp / 1000
        return CTemp

    def getSoftTemps(self):
        # CAREFUL! This doesn't recheck, it relies on the sensor's last value.
        # Important because if a logic check on a recent value triggered
        # action, we don't want to recheck and then act on a different value.
        temps = {'C', self.getCTemp()}
        temps['F'] = temps['C'] * 1.8 + 32
        temps['CString'] = str(temps['C'])[:7] + 'C'
        temps['FString'] = str(temps['F'])[:7] + 'F'
        return temps
