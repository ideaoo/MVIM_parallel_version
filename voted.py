from ovito.io import import_file
from ovito.io import export_file
from ovito.modifiers import *
from ovito.data import *
from ovito.data import NearestNeighborFinder
import numpy as np
import pandas as pd

#input file
#path1 = 'D:/pre_size1_mvim'
file_path = 'C:/Users/smcmlab-24/Desktop/sop_test/classify_test/MVIM_test/post_50_*.dump'
node = import_file(file_path)

def vote_your_variant(frame, data, pass_score, score_array, initial_variant_array):
	N = 12
	finder = NearestNeighborFinder(N, data)
	variant = initial_variant_array.astype(int)
	score = 23 + pass_score
	for i in range(variant.shape[0]):
		if variant[i] == 23:
			variant[i] = 23 + score_array[i]
	itera_time = 0
	while int(np.max(variant)) > score and itera_time < 100 :
		for index in range(data.particles.count) :
			if variant[index] > score:
				vote_box = []
				neighbors = [ neigh.index for neigh in finder.find(index) ]
				for nei_index in neighbors :
					vote_box.append(int(variant[nei_index]))
				vote_box = np.array(vote_box)
				new_variant = np.argmax(np.bincount(vote_box))
				if new_variant < 23 : 
					variant[index] = new_variant
		itera_time = itera_time + 1
		#print(np.bincount(variant)[57])
	print('Hi')
	for recover in range(data.particles.count) :
		if variant[recover] > 23 :
			variant[recover] = 23
	variant = variant.tolist()
	return variant

for frame_index in range(0,node.source.num_frames,1):
	data = node.compute(frame_index)
	initial_variant_list = data.particles_['variant']
	initial_variant_array = np.array(initial_variant_list)
	score_list = data.particles_['score']
	score_array = np.array(score_list)
	vote = vote_your_variant(frame_index, data, 9, score_array, initial_variant_array)
	data.particles_.create_property('Variants', data = vote)
	export_file(data,'C:/Users/smcmlab-24/Desktop/sop_test/classify_test/vote/vote_%s.dump'%frame_index, 'lammps/dump', columns = ['Particle Identifier','Particle Type','Position.X', 'Position.Y', 'Position.Z','Variants'],frame = frame_index)
