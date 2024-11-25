from numpy import float64
import pandas as pd    
from ovito.io import *
from ovito.modifiers import *
from ovito.data import *
import os


#the path of the two import files
for i in range(0,2):
    
    header_file = "D:/parallel_mvim/new_2/decimal_arranged/average_arrange_%s.dump"%(i)

    #the path of the final file
    
    path2 = "D:/parallel_mvim/new_2/decimal_arranged/part%s"%(i)
    
    for x in range(0,8):
        file = path2+'/file_%s.dump'%(x)
        
        file1 = open(file,'r')

        Bars = []

        data = open(header_file,'r')

        for i in range (9):
            line = data.readline()
            Bars.append(line)
        data.close()

        Atoms_line = Bars[3]

        df = pd.read_csv(file, sep='\s+', header = None, float_precision = 'high')

        with open(path2+'/combine_%s.dump'%(x),'w') as f:

            num = str(len(df.index))+'\n'
            num_1 = int(num)
            Bars1 = [num if a == Atoms_line else a for a in Bars]
            StrA = "".join(Bars1)
            f.write(StrA)
            
            for i in range(0,num_1):
                
                info = file1.readline()

                f.write(info)
            
        #os.remove(file)