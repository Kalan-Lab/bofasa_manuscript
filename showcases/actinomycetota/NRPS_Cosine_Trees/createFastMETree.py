import os
import sys
from collections import defaultdict
import numpy as np
from scipy.spatial import distance
from ete3 import Tree

nrps_file = 'NRPS_Locus_Tags.txt'
dog_mat_file = 'Domain_Ortholog_Groups.tsv'

prots = set([])
with open(nrps_file) as onf:
    for line in onf:
        line = line.strip()
        prots.add(line.split('\t')[-1])

dogs = set([])
prot_dogs = defaultdict(lambda: defaultdict(int))
with open(dog_mat_file) as odmf:
    for i, line in enumerate(odmf):
        line = line.strip('\n')
        ls = line.split('\t')
        if i == 0: continue
        dog = ls[0]
        for doms in ls[1:]:
            for dom in doms.split(','):
                if dom.strip() != '':
                    prot = dom.split('|')[1]
                    if prot in prots:
                        prot_dogs[prot][dog] += 1
                        dogs.add(dog)

prot_dog_vectors = defaultdict(list)
for p in prots:
    for d in sorted(dogs):
        prot_dog_vectors[p].append(prot_dogs[p][d])
				
prot_dog_vectors_np = {}
for p in prot_dog_vectors:
    prot_dog_vectors_np[p] = np.array(prot_dog_vectors[p])
	
cog_dist_file = 'Cosine_Distance_Matrix.txt'
naming = {}
outf = open(cog_dist_file, 'w')
outf.write(str(len(prot_dog_vectors_np.keys())) + '\n')
for p1i, p1 in enumerate(sorted(prot_dog_vectors_np)):
    p1_dist = []
    for p2 in sorted(prot_dog_vectors_np):
        dist = distance.cosine(prot_dog_vectors_np[p1], prot_dog_vectors_np[p2])
        p1_dist.append(str(dist))
    len_id = len(str(p1i))
    assert(10 > len_id)
    naming[str(p1i)] = p1
    name = str(p1i) + (' '*(10-len_id))
    outf.write(name + ' '.join(p1_dist) + '\n')
outf.close()

tre_file = 'NRPS_FastME.tre'
fastme_cmd = ['fastme', '-i', cog_dist_file, '-o', tre_file, '-T', '30']
os.system(' '.join(fastme_cmd))

t = Tree(tre_file)
for n in t.traverse('postorder'):
    if n.is_leaf():
        n.name = naming[n.name]

t.write(outfile='NRPS_FastME.named.tre')
