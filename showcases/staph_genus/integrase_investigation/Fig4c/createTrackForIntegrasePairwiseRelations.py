import os
import sys
from collections import defaultdict
from ete3 import Tree

all_prots = set([])
pair_relations = defaultdict(lambda: defaultdict(lambda: 0.0))
with open('Reflexive_Blast.txt') as orbf:
    for line in orbf:
        line = line.strip('\n')
        ls = line.split('\t')
        q = ls[0]; s = ls[1]; pid = float(ls[2]); qcov = float(ls[-1])
        if qcov < 25.0: continue
        pair_relations[q][s] = pid
        all_prots.add(q)

print('DATASET_HEATMAP')
print('SEPARATOR TAB')
print('DATASET_LABEL\tIdentity')
print('COLOR\t#000000')
print('FIELD_LABELS\t' + '\t'.join(sorted(all_prots)))
print('DATA')

for p in all_prots:
    print(p + '\t' + 

