# 12.07.17
# Porthmeus
import warnings
import constants as ct

class Polyp:
    '''Class definition for a polyp as foundation for the whole simulation'''

    def __init__(self, startcells = 1000, proliferation = 0.8, tau = 72, max = 20000, budSize = 0.45, budDevTime = 72, birth = 0, apoptosis = 0.17, tau2 = 72, unit = "h", stepSize = 1, ID = "a.1"):
        ''' 
        @startcells the polyp starts with this amount of cells
        @proliferation the amount of cells that devide in the given time
        constant tau. [0 < proliferation < 1]
        @tau the time constant which defines the time for the in which
        proliferation in quantized
        @max the number of cells when a polyp decides to bud
        @budSize either a value between 0 and 1, giving the fraction of the
        mother polyps maximal size for the size definition of the resulting bud
        or a value larger than 1 giving a discrete number for the resulting
        budSize
        @budDevTime the time a bud needs to develop and drop after initiation.
        Be aware of the time units, has to be the same as tau
        @birth this value is important for simulation with several animals,
        when during the simulation was this polyp dropped from the mother polyp
        @apoptosis giving the rate of apoptotic cell in a given time frame
        tau2. [0 < apoptosis < 1]
        @tau2 giving the time constant for the apoptosis rate. 
        @unit the time unit used, usually 'd' or 'h' (default = h). This value
        has no real effect, it is just for information.
        '''
         

        self.buds = []
        # initialize starting conditions
        if startcells < 0:
            raise ValueError("The polyp has to have more than 1 cell to start with")
        else:
            if type(startcells) is not int:
                warnings.warn("startcells is not an integer, will be rounded and converted")
                startcells = int(round(startcells))
                
            self.startcells = startcells
            self.size = startcells
        
        if 0 < proliferation <= 1:
            self.proliferation = proliferation
        else:
            raise ValueError("Proliferation rate must be a value between 0 and 1")
        
        if tau > 0:
            self.tau = tau
        else:
            raise ValueError("tau must be >0")
        
        if max > 0:
            self.max = max
        else:
            raise ValueError("max must be >0")

        if 1 > budSize > 0:
            self.budSize = budSize
        elif budSize > 1:
            self.budSize = budSize
        else:
            raise ValueError("budSize must be either a value between 0 and 1 or a whole number larger than 1")

        if budDevTime > 0:
            self.budDevTime = budDevTime
        else:
            raise ValueError("budDevTime must be >0")
        
        self.birth = birth
        self.current = birth
        
        if 0 < apoptosis <= 1:
            self.apoptosis = apoptosis
        else:
            raise ValueError("apoptosis must be a value between 0 and 1")

        if tau2 > 0:
            self.tau2 = tau2
        else:
            raise ValueError("tau2 must be > 0")


        self.unit = unit
        self.stepSize = stepSize
        self.budPortion = round((float(self.budSize)/self.budDevTime)/self.stepSize)
        
        
        # give the polyp a name

        self.ID = ID

        # initialize some variables of the object
        self.droppedBuds = {}
        self.sizeDic = {self.current : self.size}

        # do some checking of data input

        if tau/budDevTime > 10 or budDevTime/tau > 10:
            warnings.warn("tau and budDevTime differ one order of magnitude, please check the units! Unit is given as '{unit}'".format(unit=self.unit))

    
    def __str__(self):
        text ='''
ID             {ID}
Birth          {birth}
# Cells:       {cells}
Current time : {time}
# Buds:        {buds}'''.format(ID=self.ID, birth= self.birth, cells = int(round(self.size)), time = self.current, buds= len(self.buds))
        return(text)

    def simStep(self):
        
        ''' do the next step in the simulation '''
        droppedBuds = []
        self.current = self.current + self.stepSize
        # calculate the amount of apoptotic and proliferating cells 
        prol = ((self.proliferation/self.tau) + 1)/self.stepSize
        apop = (self.apoptosis/self.tau2)/self.stepSize

        # calculate the amount of cells which is lost in buds and check whether
        # a bud needs to be dropped
        budloss = 0
        dels = []
        for i,b in enumerate(self.buds):
            budloss = budloss + b.simStep()
            
            if 0 < self.budSize < 1:
                b.max = round(self.size*self.budSize)
            if b.size > b.max:
                droppedBuds.append(b.drop())
                #print("dropped bud")
                self.droppedBuds[b.ID]=self.current
                dels.append(i)

        # remove the droped buds from the list
        dels.reverse()
        for i in dels:
            del self.buds[i]

        
        # calculate the current size and add the current life time of the polyp
        self.size = self.size - budloss
        self.size = (self.size * prol) - (self.size * apop)

        # check whether a bud has to be initiated
        if self.size > self.max:
            self.initiateBud()
        

        # store the size data in a dic
        self.sizeDic[self.current] = self.size
        return(droppedBuds)
        

    
        

    def initiateBud(self):
        ''' 
        create a bud, put it in the budlist and reduce the size by the first
        budstep
        '''
        
        if 0 < self.budSize < 1:
            bMax = round(self.budSize * self.size)
        else :
            bMax = self.budSize
        

        # generate the bud name
        ID = self.ID.split(".")
        gen = ct.generation.index(ID[0])
        num = len(self.droppedBuds) + len(self.buds)+1
        
        i = -2
        while gen+1 > len(ct.generation):
            i = i+1
            gen = gen - 26
            if i > len(ct.generation):
                raise ValueError("To many generations created (>67,108,864). ABORTED!")
        if i > 0:
            gen = "".join([ct.generation[gen+1],ct.generation[i]])
        else:
            gen = ct.generation[gen+1]

        IDb = [gen]
        IDb.extend(ID[1:])
        IDb.append(str(num))
        IDb = ".".join(IDb)
        #print(IDb)

        # add initialize the bud and store it in the buds list
        self.buds.append(
            Bud(startcells = self.budPortion,
                proliferation = self.proliferation,
                tau = self.tau,
                max= self.max,
                budSize= bMax,
                budDevTime = self.budDevTime,
                birth = self.current,
                apoptosis = self.apoptosis,
                tau2 = self.tau2,
                unit=self.unit,
                stepSize = self.stepSize,
                ID = IDb))
        
        # reduce the cell number by the budPortion
        self.size = self.size - self.budPortion
        






class Bud(Polyp):
    ''' A class for buds on a polyp. Inherits from Polyp. '''

    def __init__(self,
        startcells = 450,
        proliferation = 0.8,
        tau = 72,
        max = 20000,
        budSize = 0.45,
        budDevTime = 72,
        birth=0,
        apoptosis = 0.1,
        tau2 = 72,
        unit = "h",
        stepSize = 1,
        ID = "a.1"):

        Polyp.__init__(self,
            startcells = startcells,
            proliferation = proliferation,
            tau = tau,
            max = max,
            budSize = budSize,
            budDevTime = budDevTime,
            birth = birth,
            apoptosis = apoptosis,
            tau2 = tau2,
            unit = unit,
            stepSize = stepSize,
            ID = ID)
        
        # redefine some small things
        self.adultMax = self.max
        self.max = self.budSize
        
    def simStep(self):
        ''' do the next step in the simulation and return a value of cells coming from the mother polyp '''

        self.current = self.current + self.stepSize
        # calculate the amount of apoptotic and proliferating cells 
        prol = ((self.proliferation/self.tau) + 1)/self.stepSize
        apop = (self.apoptosis/self.tau2)/self.stepSize

        # calculate the current size and add the current life time of the polyp
        self.size = round(self.size * prol) - round(self.size * apop) + self.budPortion

        return(self.budPortion)

    def drop(self):
        ''' Create a new polyp with the values stored in this bud object'''

        p = Polyp(startcells=self.size,
        proliferation = self.proliferation,
        tau = self.tau,
        max= self.adultMax,
        budSize= self.max,
        budDevTime = self.budDevTime,
        birth = self.current,
        apoptosis = self.apoptosis,
        tau2 = self.tau2,
        unit = self.unit,
        stepSize = self.stepSize,
        ID = self.ID)

        return(p)


