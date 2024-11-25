# Import standard Python and NumPy modules.
from ovito.io import *
from ovito.modifiers import *
from ovito.data import *
import datetime

starttime = datetime.datetime.now() 
# Load the simulation dataset to be analyzed.
pipeline = import_file("E:/MVIM_statistic/motion/size3/equ_*.dump")

print("123")

# Loop over particles and print their CNA indices.
for series in range(pipeline.source.num_frames):
    pipeline.modifiers.append(SelectTypeModifier(property='Particle Type', types={3}))
    pipeline.modifiers.append(DeleteSelectedModifier())
    data = pipeline.compute(series)
    export_file(data, 'E:/MVIM_statistic/motion/size3/equ-wo3_%s.dump'%series, 'lammps/dump',
                columns = ['Particle Identifier','Particle Type','Position.X','Position.Y','Position.Z'],frame = series)

endtime = datetime.datetime.now()
print (endtime - starttime)	
print("Done.")