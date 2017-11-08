#!/usr/bin/python
# Porthmeus
# 01.11.17
from src.Polyp2 import Polyp
from src.simulation import *
from src.analyseSimulation import *
from src.dic2csv import dic2csv
import src.readDocumentation
import warnings
import argparse


def readKeywordValue(line):
    '''
    Small helper function to read a keyword - value pair from a line
    '''
    kv = line.replace(" ","").replace("\t","").split("=")
    
    return(kv)

def nonblank_lines(f):
    '''
    Helper for kicking out blank lines
    '''
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def parseInitiation(config):

    '''
    Takes a config file for HyPy, reads the Initiation part and returns a list
    of polyps for initiation of the simulation.
    @ config - the location of the config file
    '''

    # list of keyvalues for polyp initiation
    keyCheck = ["startcells","proliferation","tau","max","budSize","budDevTime","birth","apoptosis","tau2","unit","stepSize"]

    polyps = []

    read = False
    polyp = False
    nPolyp = 0
    # open the file and start reading
    with open(config, "r") as cfg:
        for l in nonblank_lines(cfg):
            l = l.strip("\n")
            
            # ignore comments
            if not l.replace(" ","").startswith("#") or not l.strip() == "":
                
                # get the initiation part
                if l.startswith("%"):
                    part = l.replace(" ","").replace("%","")
                    if part.lower() == "initiation":
                        read = True
                    else:
                        read = False
                
                # read the polyps
                if read:
                    if l.startswith(">"):
                        # if there is a new polyp and an old was initiatiated
                        # already, add it to the polyps list
                        if nPolyp > 0:
                            polyps.append(Polyp(**plp))
                        
                        # create a dictionary to store the values
                        plp = {}    
                        name = l.replace(" ","").replace(">","")
                        plp["ID"] = "a." + str(nPolyp + 1)
                        nPolyp = nPolyp +1
                    
                    # get the whole polyp information which is given
                    else:
                        if l.startswith(" ") or l.startswith("\t"):
                            kv = readKeywordValue(l)
                            if kv[0] in keyCheck:
                                if kv[0] == "unit":
                                    plp[kv[0]] = kv[1]
                                elif kv[0] == "birth":
                                    plp[kv[0]] = int(kv[1])
                                else:
                                    plp[kv[0]] = float(kv[1])
                            else:
                                warnings.warn("Key {key} is no value for initiation of a polyp and will be ignored. The allowed keys are the following: {keys}".format(key = kv[0], keys = str(keyCheck).strip("[|]")))
    
    # add the last polyp or generate a generic one if there is no polyp nor initiation part in the config file
        
    if nPolyp == 0:
        polyps.append(Polyp())
    else:
        polyps.append(Polyp(**plp))
    
    

    return(polyps)
    

def parseSimulation(config, polyps):
    '''
    Read the simulation part of the config file, set it up and let it run.
    @ config - the path to the config file
    @ polyps - a list of polyps for the initiation of the simulation

    returns a list of polyp
    '''
    
    byTime = None
    byNumber = None
    time = None
    number = None


    read = False
    # open the file and start reading
    with open(config, "r") as cfg:
        for l in nonblank_lines(cfg):
            l = l.strip("\n")
            
            # ignore comments
            if not l.replace(" ","").startswith("#") or not line.strip() == "":
                
                # get the initiation part
                if l.startswith("%"):
                    part = l.replace(" ","").replace("%","")
                    if part.lower() == "simulation":
                        read = True
                    else:
                        read = False

            # read the simulation
            if read:
                kv = readKeywordValue(l)

                if kv[0] == "byTime":
                    if kv[1].lower() == "false":
                        byTime = False
                    elif kv[1].lower() == "true":
                        byTime = True
                    else:
                        warnings.warn("byTime keyword must be followed by true or false argument! byTime is set to false")
                        byTime = False

                if kv[0] == "byNumber":
                    if kv[1].lower() == "false":
                        byNumber = False
                    elif kv[1].lower() == "true":
                        byNumber = True
                    else:
                        warnings.warn("byNumber keyword must be followed by true or false argument! byTime is set to false")
                        byNumber = False

    
                if kv[0].lower() == "number":
                    number = int(kv[1])
                if kv[0].lower() == "time":
                    time = int(kv[1])
        
        # if nothing is given make simulation until 20 polyps are reached
        if byTime == None and byNumber == None:
            byNumber = True
            if number == None:
                number = 20
        
        # simulate 100 timesteps if no time is given, but time should be simulated
        if byTime == True and time == None:
            time = 100

        # simulate 20 Polyps if no number is given, but polyp number should be simulated
        if byNumber == True and number == None:
            number = 20

        # check which simulation should be performed and simulate
        if byNumber and byTime:
            simu = simulateTimeNumber(time, number, polyps)
        elif byNumber:
            simu = simulateNumber(number, polyps)
        elif byTime:
            simu = simulateTime(time, polyps)


        # return it
        return(simu)


def parseAnalysis(config, polyps):
    '''
    Parse the analysis part of the config file and do the analysis

    @ config - the path to the config file
    @ polyps - the list of polyps after the simulation

    returns... nothing, but produces the output files specified in the config file
    '''
    # the list to check valid keywords
    check = ["cellnumber", "population", "families", "deltats", "budinitiation", "buddrops"]
    
    # some variables
    read = False
    family = False
    generation = "a"
    cutoff = 5

    # just print the files written during the process
    ff = []
    # open the file and start reading
    with open(config, "r") as cfg:
        for l in nonblank_lines(cfg):
            l = l.strip("\n")
            
            # ignore comments
            if not l.replace(" ","").startswith("#") or not line.strip() == "":
                
        


                # read the file and do the analysis
                if read:
                    kv = readKeywordValue(l)
                    # if population growth should be calculated read possible options indicated with the indentation
                    if family:
                        if l.startswith(" ") or l.startswith ("\t"):
                            kv = readKeywordValue(l)
                            if kv[0].lower() == "generation":
                                generation = kv[1]
                            elif kv[0].lower() == "cutoff":
                                cutoff = float(kv[1])
                            else:
                                warnings.warn("Keyword {key} does not apply to any option for population growth calculation for different families. Please use 'generation' to define the generation where the simulation should be splitted in single families and 'cutoff' to discard families smaller than the number given here".format(key = kv[0]))
                        else:
                            df = getPopGrowths(polyps, generation = generation, cutoff = cutoff)
                            df.to_csv(family)
                            ff.append(family)
                            family = False
                    
                    # read the different analysis types which should be carried out and perform the analysis
                    if kv[0].lower() in check:
                        
                        if kv[0].lower() == "cellnumber":
                            df = getCells(polyps)
                            df.to_csv(kv[1])
                            ff.append(kv[1])
                        elif kv[0].lower() == "population":
                            family = kv[1]
                        elif kv[0].lower() == "budinitiation":
                            df = getBudInitiationDates(polyps)
                            df.to_csv(kv[1])
                            ff.append(kv[1])
                        elif kv[0].lower() == "buddrops":
                            df = getBudDroppingDates(polyps)
                            df.to_csv(kv[1])
                            ff.append(kv[1])
                        elif kv[0].lower() == "deltats":
                            df = getDeltaTs(polyps)
                            df = dic2csv(df, kv[1])
                            ff.append(kv[1])

                    elif family:
                        print("reading...")
                    else:
                        warnings.warn("The keyword {key} is not defined for analysis and will be ignored. These analyis can be run: {keys}".format(key = kv[0], keys = str(check).strip("[|]")))
                
                # get the analysis part
                if l.startswith("%"):
                    part = l.replace(" ","").replace("%","")
                    if part.lower() == "analysis":
                        read = True
                    else:
                        read = False
    ff.sort()
    print("Analysis done! Written the following files: {ff}\n".format(ff = str(ff).strip("[|]")))


if __name__ == "__main__":
    

    configFileDoc = src.readDocumentation.readConfigDoc()

    aprs = argparse.ArgumentParser(version = "1.0",
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = configFileDoc)
    aprs.add_argument("config", help = "The path to the config file")

    args = aprs.parse_args()
    

    print("Initializing\n")
    polyps = parseInitiation(args.config)
    print("Done\nSimulating\n")
    polyps = parseSimulation(args.config, polyps)
    print("Done\nAnalyzing data\n")
    parseAnalysis(args.config, polyps)
    print("Done\n")

