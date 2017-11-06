from Polyp2 import Polyp
import numpy as np
from simulation import *
from analyseSimulation import *
import pandas as pd


a = Polyp(startcells=11320, budSize=0.54, budDevTime=3.6*24, max=20871, tau = 72, proliferation=0.6781660783 )
a2 = Polyp(startcells = 10000, budSize = 0.46, budDevTime = 3.5*24, max=20000, tau = 72, proliferation = 0.6, ID = "a.2", birth =3)
a = [a,a2]
d = simulateNumber(300,a)
df = getCells(d)
df.to_csv("TestDF.csv")
g = getPopGrowths(d)
dt = getDeltaTs(d)
budIni = getBudInitiationDates(d)
budIni.to_csv("BudIni.csv")
budDrop = getBudDroppingDates(d)
budDrop.to_csv("BudDrop.csv")

for key in dt.keys():
    print(key + " : "+ str(np.nanmean(dt[key])/24))
    

