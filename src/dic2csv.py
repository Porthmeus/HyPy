
def dic2csv(dic, outfile, sep=','):
    '''
    takes values of a dictionary an writes an csv file with the keys as header

    this wont work if the value of a dictionary is an array
    '''
    
    # create a new dictionary (Ndic) similar to input dictionary but with
    # values being lists
    Ndic={}
    for keys,val in dic.items():
        
        if type(val)!=list and type(val)!=tuple:
            lst=[val]
        elif type(val)==tuple:
            lst=list(val)
        else:
            lst=val
        
        Ndic[keys]=lst
    
    # find longest list in Ndic
    maxLength=0
    for val in Ndic.values():

        if len(val)>maxLength:
            maxLength=len(val)
    
    # append the lists which are smaller than the longest with '<NA>'

    for keys, val in Ndic.items():

        while len(val)<maxLength:
            val.append("nan")

        Ndic[keys]=val

    # create string to write in the csv file

    header=''#str(Ndic.keys()).replace('[','').replace(']','').replace("'",'')
    for key in Ndic.keys():
        header+=key+sep
    values=''
    for i in range(0,maxLength):
        values+='\n'
        for key in Ndic.keys():
            val=Ndic[key]
            values+=str(val[i])+sep
        values=values.rstrip(sep)
    
    header=header.rstrip(sep)
    csv=header+values

    # write csv

    with open(outfile,'w') as ff:
        ff.write(csv)

    return Ndic
