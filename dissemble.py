import pandas as pd    
import numpy as np
from ovito.io import *
from ovito.modifiers import *
from ovito.data import *
import datetime

starttime = datetime.datetime.now()

for x in range(0,8):

#the path of the two import files
    path = 'D:/parallel_mvim/new_2/0118_voted/vote_%s.dump'%(x)
    pathA = 'D:/parallel_mvim/new_2/part1/ref_%s.dump'%(x)

    #the path of the final file
    pathB = "D:/parallel_mvim/new_2/0118_final"

    Bars = []

    data = open(path,'r')

    for i in range (9):
        line = data.readline()
        Bars.append(line)
    print(Bars)
    data.close()

    Atoms_line = Bars[3]
    natoms = int(Atoms_line)
    print(natoms)

    df0 = pd.read_csv(path, skiprows=9 , sep='\s+' , header = None)

    df1 = pd.read_csv(pathA, sep='\s+', header = None)

    data_csv = pd.concat([df0, df1], ignore_index=True, sort=False)
    print(data_csv)

    df_without_duplicates = data_csv.drop_duplicates(subset=[0],keep=False)

    with open(pathB+'/segment_%s.dump'%(x),'w') as f:

        num = str(len(df_without_duplicates.index))+'\n'
        Bars1 = [num if a == Atoms_line else a for a in Bars]
        StrA = "".join(Bars1)
        f.write(StrA)
        f.write(df_without_duplicates.to_string(index=False,header=False))
   
        
for i in range(0,8):
    
    globals()['path'+str(i)] = pathB+'/segment_%s.dump'%(i)

Bars = []
data = open(path0,'r')

for i in range (9):
    line = data.readline()
    Bars.append(line)
print(Bars)
data.close()
Atoms_line = Bars[3]

df0 = pd.read_csv(path0, skiprows=9 , sep='\s+', header = None)

df1 = pd.read_csv(path1, skiprows=9 , sep='\s+', header = None)

df2 = pd.read_csv(path2, skiprows=9 , sep='\s+', header = None)

df3 = pd.read_csv(path3, skiprows=9 , sep='\s+', header = None)

df4 = pd.read_csv(path4, skiprows=9 , sep='\s+', header = None)

df5 = pd.read_csv(path5, skiprows=9 , sep='\s+', header = None)

df6 = pd.read_csv(path6, skiprows=9 , sep='\s+', header = None)

df7 = pd.read_csv(path7, skiprows=9 , sep='\s+', header = None)

data_csv = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7], ignore_index=True, sort=False)
    

with open(pathB+'/mvim_final.dump','w') as f:

    num = str(len(data_csv.index))+'\n'
    Bars1 = [num if a == Atoms_line else a for a in Bars]
    StrA = "".join(Bars1)
    f.write(StrA)
    f.write(data_csv.to_string(index=False,header=False))
        
endtime = datetime.datetime.now()
print (endtime - starttime)