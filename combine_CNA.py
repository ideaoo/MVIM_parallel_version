import datetime
import os
from ovito.io import *
from ovito.modifiers import *
from ovito.data import *
import numpy as np
import sys
import scipy.linalg as sl
import math

    
starttime = datetime.datetime.now()

for x in range(9,10):
    globals()['path_'+str(x)] = "C:/Users/smcmlab-24/Desktop/sop_test/classify_test/ref.dump"
    #%(x)
    
    # the folder of the final files
    globals()['path'+str(x)] = "C:/Users/smcmlab-24/Desktop/sop_test/classify_test/ref"
    #%(x)

final_path = "/work/p00sim00/py_test/pre_size3/final"


# the pieces to be divided 
pieces = 8

for x in range(9,10):

# Read the information of the header
    Bars = []
    data = open(globals()['path_'+str(x)],'r')

    for i in range (9):
        line = data.readline()
        Bars.append(line)
    Atoms_line = Bars[3]


    # Combine the reference and the target file
    for i in range(0,pieces):

        locals()['counter'+str(i)] = 0 
        locals()['count'+str(i)] = 0

        with open(globals()['path'+str(x)]+'/file_%s.dump'%(i), 'r+') as filedata:

            for index, line in enumerate(filedata):
                locals()['counter'+str(i)] += 1
                locals()['count'+str(i)] += 1

        with open(globals()['path'+str(x)]+'/ref_%s.dump'%(i), 'r+') as filedata2:

            for index, line in enumerate(filedata2):
                locals()['counter'+str(i)] += 1



        with open(globals()['path'+str(x)]+'/combine_%s.dump'%(i),'w') as outfile:

            num = str(locals()['counter'+str(i)])+'\n'
            Bars1 = [num if a == Atoms_line else a for a in Bars]
            StrA = "".join(Bars1)
            outfile.write(StrA)
            
            filedata = open(globals()['path'+str(x)]+'/file_%s.dump'%(i),'r')
            data = filedata.readlines()
            for line in data :
                outfile.write(line)
            filedata.close()

            filedata2 = open(globals()['path'+str(x)]+'/ref_%s.dump'%(i),'r')
            data2 = filedata2.readlines()
            
            for line in data2 :
                outfile.write(line)
            filedata2.close()


    # Common neighbor analysis 
    pipeline = import_file(globals()['path'+str(x)]+'/combine_*.dump')

    # Loop over particles and print their CNA indices.
    for series in range(pipeline.source.num_frames):

        pipeline.modifiers.append(CommonNeighborAnalysisModifier(
        mode = CommonNeighborAnalysisModifier.Mode.AdaptiveCutoff))
        data = pipeline.compute(series)

        export_file(data, globals()['path'+str(x)]+'/cna_%s.dump'%series, 'lammps/dump',columns = ['Particle Identifier','Particle Type','Position.X','Position.Y','Position.Z','Structure Type'],frame = series)


    # Read the information of the header
    BarsX = []
    data = open(globals()['path'+str(x)]+'/cna_0.dump','r')

    for i in range (9):

        line = data.readline()
        BarsX.append(line)

    Atom_line1 = BarsX[3]

    COUNT = 0
    for i in range(0,pieces): 
        COUNT += locals()['count'+str(i)]

    print(COUNT)

    # Recombine the model
    with open (final_path+'/final_%s.dump'%(x),'w') as filedata:

        num = str(COUNT)+'\n'
        Bars1 = [num if a==Atom_line1 else a for a in BarsX]
        StrB = "".join(Bars1)
        filedata.write(StrB)

        for i in range(0,pieces): 

            node = open(globals()['path'+str(x)]+'/cna_%s.dump'%(i),'r')

            for line in range (1,locals()['count'+str(i)]+11):

                    lines_after_9 = node.readline()

                    if 9 < line < locals()['count'+str(i)]+10:

                        filedata.write(lines_after_9)
            
            node.close()




    for i in range (0, pieces):
        os.remove(globals()['path'+str(x)]+'/file_%s.dump'%(i))
        os.remove(globals()['path'+str(x)]+'/ref_%s.dump'%(i))
        os.remove(globals()['path'+str(x)]+'/combine_%s.dump'%(i)) 
   

 
for x in range(35000,45001,5000):
    for i in range (0,pieces):
        os.remove(globals()['path'+str(x)]+'/cna_%s.dump'%(i))
 

endtime = datetime.datetime.now()
print(endtime - starttime)
print("done")

