from subprocess import Popen
import time

def startServer(serverType):
    serverType = 'indi_' + serverType.replace(' ', '_').lower()
    Popen(['bash', './bash/server.sh', serverType])

def killServer():
    Popen(['bash', './bash/kill.sh'])
