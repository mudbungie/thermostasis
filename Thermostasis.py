from time import sleep
from Thermconfig import config
import Pod

def initializeAllPods():
    pods = {}
    for label, definition in config['pods'].items():
        pods[label] = Pod(label)
    return pods

def checkAllPods(pods):
    for pod in pods.items():
        pod.checkTolerance()

if __name__ == '__main__':
    pods = initializeAllPods()
    while True:
        checkAllPods(pods)
        time.sleep(1)
