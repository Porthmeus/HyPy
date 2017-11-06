# 18.07.17
# Porthmeus

import pandas as pd
from Polyp2 import Polyp
import copy


def getCells(simulationList):
    '''
    Calculates the cellnumber for each timepoint and polyp in a simulation from
    the list of simulated polyps.

    @ simulationList the list with the polyp objects
    
    Returns:
        * a pandas dataframe with time steps as rows and the polyps as columns
          containing the cell number at the given time
    '''
    
    data = {}
    for p in simulationList:
        data[p.ID] = p.sizeDic

    df = pd.DataFrame(data)
    return(df)


def getPopGrow(simulationList):
    '''

    Extracts the number of polyp at a given time from the list of polyps from a
    simulation.
    '''
    # get all the birth dates
    births = []
    for p in simulationList:
        births.append(int(p.birth))
    
    # from that calculate the span of simulation
    start = 0
    end = p.current - min(sorted(births)[1:])
    correction = min(sorted(births)[1:])
    # create a dictionary from this
    growthDic = {}
    polyps = 0
    for i in range(start, int(end)+1, p.stepSize):
        j = i + correction
        for b in births:
            if b == j:
                polyps = polyps+1
        growthDic[i] = polyps
    
    return(growthDic)


def splitSimulationListByGeneration(simulationList, generation = "b"):
    '''

    Splits the simulation polyps list into several small lists where the
    founder of the resulting lists come all from the same generation
    
    @simulationList the polyps list from a simulation
    @generation the generation on which the split should occur

    returns:
        * a dictionary with founder ID as key and list of polyps in this family
          as value
    '''

    # find all the founder polyps
    founders = []
    for polyp in simulationList:
        if list(polyp.ID)[0] == generation:
            founders.append(polyp.ID)

    if len(founders) == 0:
        raise ValueError("No polyps of generation {gen} found in the polyps list".format(gen = generation))


    # go and find the family members
    familyDic = {}
    for founder in founders:
        familyDic[founder] = []
        stem = ".".join(founder.split(".")[1:])
        famEnd = len(stem.split("."))+1
        for polyp in simulationList:
            family = ".".join(polyp.ID.split(".")[1:famEnd])
            if stem == family:
                familyDic[founder].append(polyp)

    return(familyDic)

def getPopGrowths(simulationList, generation = "b", cutoff = 5):
    '''
    
    The function takes a list of polyp objects from a simulation, splits it
    into family list with founders coming from one generation and returns a
    data frame with the population growth for each of the family.
    
    @ simulationList a list of polyps from a simulation
    @ generation the generation which the polyps should be drawn which
      constitute the founderst of the different families
    @ cutoff defines how many members a family has to have to be make it in the
      list 
    
    returns:
        * a data frame with the ID of the founder polyp as column and the time
          points of the simulation in the rows.
    '''

    families = splitSimulationListByGeneration(simulationList = simulationList,
        generation = generation)
    
    data = {}
    for founder in families.keys():
        if len(families[founder]) >= cutoff:
            data[founder] = getPopGrow(families[founder])

    data = pd.DataFrame(data)

    return(data)

def getDeltaTs(simulationList):
    '''

    The function returns a dictionary containing the values of all
    developmental time points from all polyps in the given simulation as a list
    of integers. The developmental time points are:
        * dT1 is the time from a dropped bud to an adult polyp which is
          initiating its first bud as well
        * dT2 is the time from bud initiation to the dropped bud
        * dT3 is the time between to initiations

    @simulationList a list of polyps from a simulation
    
    returns:
        * a dictionary of the different dT lists
    '''

    deltas = {"dT1" : [], "dT2" : [], "dT3" : []}

    for polyp in simulationList:
        dTs = polyp.getDeltaT()
        
        deltas["dT1"].append(dTs["dT1"])
        deltas["dT2"].extend(dTs["dT2"].values())
        deltas["dT3"].extend(dTs["dT3"])

    return(deltas)

def getBudInitiationDates(simulationList):
    ''' Takes all polyps from a simulation and puts their bud initations into a dataframe 
        @ simulationList a list of polyps from the simulation
        
        returns a panda frame
    '''
    data = {}
    for polyp in simulationList:
        dic = {}
        for i in range(0, len(polyp.initializedBuds.values())):
            dic[i+1] = sorted(polyp.initializedBuds.values())[i]

        data[polyp.ID] = dic

    data = pd.DataFrame(data)
    return(data)

def getBudDroppingDates(simulationList):
    ''' Takes a simulation polyp list and puts the dates of all dropped bud into a data frame for each polyp
        @ simulationList a list of polyps from the simulation

        returns a panda frame
    '''
    data = {}
    for polyp in simulationList:
        dic = {}
        for i in range(0, len(polyp.droppedBuds.values())):
            dic[i+1] = sorted(polyp.droppedBuds.values())[i]
        
        data[polyp.ID] = dic

    data = pd.DataFrame(data)
    return(data)
    
