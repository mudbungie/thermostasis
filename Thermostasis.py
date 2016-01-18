from time import sleep
from Thermconfig import config
import Pod

def initializeAllPods():
    pods = {}
    for label, definition in config['pods'].items():
        pod = Pod.Pod(label)
        pods[label] = pod
    return pods

def checkAllPods(pods):
    for label, pod in pods.items():
        pod.checkTolerance()
        # Diagnostics
        #print(pod.thermometer.getSoftTemps()['CString'])

if __name__ == '__main__':
    pods = initializeAllPods()
    while True:
        checkAllPods(pods)
        sleep(1)
