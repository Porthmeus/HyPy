# 14.07.17
# Porthmeus
import pandas as pd
from Polyp2 import Polyp
import copy

def simulateTime(t, Polyp):
    '''
    Simulates a growth experiment for a certain time frame
    @t the amount of time units to be simulated
    @Polyp the Urmother of the simulation
    
    The function will return:
        * a list of the simulated polyps
    '''

    d=[]
    d.extend(Polyp)
    polyp = d[0]
    for p in d:
        if p.birth < polyp.birth:
            polyp = p

    for i in range(polyp.birth + polyp.stepSize, polyp.birth+t+polyp.stepSize, polyp.stepSize):
        dd = []
        for p in d:
            if p.current == i-1:
                dd.extend(p.simStep())
        d.extend(dd)
        #print(str(i) + " " + str(d))
        
    return(d)

def simulateNumber(num, Polyp):
    '''
    Simulates a growth experiment until a certain amount of polyps have been
    dropped.
    @num the number of polyps to generate in the simulation
    @Polyp the founder Polyp of the simulation

    returns:
        * a list of the simulated polyps
    '''
    # create the simulation list and add the polyps
    simulationList = []
    simulationList.extend(Polyp)
    
    # find the smallest time value of the polyp (when are the polyps added to the experiment, and which is/are the one(s) to start with)
    t=None
    for p in simulationList:
        if t==None:
            t = p.current
        else:
            if t > p.current:
                t = p.current
    

    while len(simulationList) < num:
        t = t+1
        dd=[]
        for p in simulationList:
            if p.current == t-1:
                dd.extend(p.simStep())
        simulationList.extend(dd)


    return(simulationList)
    
def simulateTimeNumber(t, num, polyp):
    '''
    Runs a simulation for both a certain time and a certain number of polyps, whatever is reached first, will stop the simulation
    @ t - number of timesteps which should be simulated
    @ num - number of polyps which should be reached
    @ polyp - the inital starting population of (or single) polyps

    returns a list of polyps after the simulation
    '''
    
    d=[]
    d.extend(Polyp)
    polyp = d[0]
    for p in d:
        if p.birth < polyp.birth:
            polyp = p

    for i in range(polyp.birth + polyp.stepSize, polyp.birth+t+polyp.stepSize, polyp.stepSize):
        dd = []
        for p in d:
            if p.current == i-1:
                dd.extend(p.simStep())
        d.extend(dd)
        #print(str(i) + " " + str(d))
        if len(d) >= num:
            break

    return(d)

