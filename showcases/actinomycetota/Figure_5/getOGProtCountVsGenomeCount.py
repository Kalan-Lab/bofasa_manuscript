import os
import sys
from collections import defaultdict
from ete3 import Tree

itol_dir = 'iTol_Tracks/'
all_prots_tre = '../NRPS_Cosine_Trees/NRPS_FastME.named.tre'
t = Tree(all_prots_tre)

all_prots = set([])
for n in t.traverse('postorder'):
    if n.is_leaf():
        all_prots.add(n.name)

print('method\tog_id\tprot_count\tgenome_count')
for f in os.listdir(itol_dir):
    method = f.split('.iTol.txt')[0]
    data = []
    with open(itol_dir + f) as oif:
        for i, line in enumerate(oif):
            line = line.strip()
            ls = line.split('\t')
            if i == 4:
                data.append(ls)
            elif i >= 6:
                data.append(ls)

    prots = []
    for i, ogi in enumerate(zip(*data)):
        if i == 0: 
            prots = ogi[1:]
            continue
        og = ogi[0]
        prot_ids = set([])
        protein_counts = 0
        for j, val in enumerate(ogi[1:]):
            pid = prots[j].split('_')[0]
            if val == '1':
                prot_ids.add(pid)
                protein_counts += 1
        genome_counts = len(prot_ids)
        if genome_counts > 1:
            print(method + '\t' + og + '\t' + str(protein_counts) +  '\t' + str(genome_counts)) 
