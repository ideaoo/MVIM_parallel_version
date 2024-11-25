import os
from ovito.io import import_file
from ovito.io import export_file
from ovito.modifiers import *
import numpy as np
import datetime

starttime = datetime.datetime.now()

#inputfile

path = 'E:/MVIM_size1/U_all/'

input_file_path = 'E:/MVIM_size1/U_all/pre_average_*.dump'

atom = import_file(input_file_path)
atom_1 = import_file(input_file_path)
atom_2 = import_file(input_file_path)

i = 0
for frame in range(atom.source.num_frames):
    data = atom.compute(frame)
    atom_1.modifiers.append(SelectTypeModifier(property= 'Particle Type', types={2}))
    atom_1.modifiers.append(DeleteSelectedModifier())
    atom_2.modifiers.append(SelectTypeModifier(property= 'Particle Type', types={1}))
    atom_2.modifiers.append(DeleteSelectedModifier())

    export_file(atom_1, path+'/c_1_%i.dump'%i, 'lammps/dump',
                columns= ['Particle Identifier', 'Particle Type', 'Position.X', 'Position.Y', 'Position.Z'], frame= i)
    export_file(atom_2, path+'/c_2_%i.dump'%i, 'lammps/dump',
                columns= ['Particle Identifier', 'Particle Type', 'Position.X', 'Position.Y', 'Position.Z'], frame= i)

    ### type1的新路徑
    new_input_file_path = path+'/c_1_*.dump'

    ### type2的新路徑
    new_input_file_path_2 = path+'/c_2_*.dump'

    ### 將type1 type2合併 ###
    arr_atom = import_file(new_input_file_path)
    modifier = CombineDatasetsModifier()
    modifier.source.load(new_input_file_path_2)
    arr_atom.modifiers.append(modifier)

    data = arr_atom.compute()
    id_list = []
    for num in range(data.particles.count):
        id_ = num+1
        id_list.append(id_)
    node_id = np.array(id_list)

    data.particles_.create_property('Particle Identifier', data = node_id)

    ### 輸出含有type1 type2的dump檔 ###
    export_file(data, path+'/average_%i.dump'%i, 'lammps/dump',
                columns= ['Particle Identifier', 'Particle Type', 'Position.X', 'Position.Y', 'Position.Z'], frame= i)

    os.remove(path+'/c_1_%s.dump'%(i))
    os.remove(path+'/c_2_%s.dump'%(i))

    i += 1


### ParticleIdentifier編號會亂跳 ###

endtime = datetime.datetime.now()
print (endtime - starttime)