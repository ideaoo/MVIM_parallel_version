from ovito.io import import_file
from ovito.io import export_file
from ovito.modifiers import *
from ovito.data import *
import numpy as np
import os
import gc
import datetime

starttime = datetime.datetime.now()


#path1 = 'E:/One_way_SMA/y_compress_325k'

# inputfile

node = import_file('E:/MVIM_size3/size3_76000/cone-325-indent-wo3_*.dump') 

count = 0
series = 0
num_average = 10
num_average_reci = 1/num_average
position_total = np.zeros(node.compute().particles_['Position_'][:].shape)

for frame_index in range(node.source.num_frames):
    data = node.compute(frame_index)
    #data.apply(WrapPeriodicImagesModifier())
    positions = np.reshape(data.particles_['Position_'],(data.particles.count,3))
    node_types = np.reshape(data.particles_['Particle Type_'],(data.particles.count,1))
    node_id = np.reshape(data.particles_['Particle Identifier'],(data.particles.count,1))
    nodes = np.hstack((node_id,node_types,positions))
    nodes = nodes[np.argsort(nodes[:,0])]
    node_position = nodes[:,2:]
    node_types = nodes[:,1]
    node_id = nodes[:,0]
    position_total =  position_total + node_position
    count = count+1
    if count%num_average == 0:
        position_total = position_total * [num_average_reci]
        count = 0
        data.particles_.create_property('Particle Identifier', data = node_id)
        data.particles_.create_property('Particle Type', data = node_types)
        data.particles_.create_property('Position', data = position_total)
        data.cell_.pbc = (True, True, False)
        export_file(data, 'E:/MVIM_size3/size3_76000/average_%s.dump'%series, 'lammps/dump',columns = ['Particle Identifier','Particle Type','Position.X','Position.Y','Position.Z'],frame = series*num_average)
        position_total = np.zeros(node_position.shape)
        gc.collect()
        series = series + 1
        
endtime = datetime.datetime.now()
print (endtime - starttime)
