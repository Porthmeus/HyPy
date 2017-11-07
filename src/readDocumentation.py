# Author: Porthmeus
# 07.11.17

import os

def readConfigDoc():
    ''' read the config.doc file and return it as string'''
    filePath = os.path.realpath(__file__)
    configFile = os.path.split(filePath)[0] + "/../doc/config.doc"
    with open(configFile, "r") as f:
        configDoc = f.read()

    return(configDoc)


