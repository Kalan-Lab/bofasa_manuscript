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


print('method\tog_type\tcount')
method_type_counts = defaultdict(lambda: defaultdict(int))
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
    accounted = set([])
    for i, ogi in enumerate(zip(*data)):
        if i == 0: 
            prots = ogi[1:]
            continue
        og = ogi[0]
        prot_ids = set([])
        for j, val in enumerate(ogi[1:]):
            pid = prots[j].split('_')[0]
            if val == '1':
                prot_ids.add(pid)
            accounted.add(prots[j])
        og_type = 'taxon-specific'
        if len(prot_ids) > 1:
            og_type = 'multi-taxon'
        elif len(prot_ids) == 0:
            sys.exit(1)
        method_type_counts[method][og_type] += 1

    for p in all_prots:
        if not p in accounted:
            og_type = 'taxon-specific'
            method_type_counts[method][og_type] += 1

    for ot in ['multi-taxon', 'taxon-specific']:
        print(method + '\t' + ot + '\t' + str(method_type_counts[method][ot]))
