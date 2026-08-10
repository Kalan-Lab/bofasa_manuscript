import os
import sys
from collections import defaultdict

nrps_file = "NRPS_Locus_Tags.txt"

bgc_prots = defaultdict(set)
with open(nrps_file) as osnf:
    for line in osnf:
        line = line.strip()
        gca, bgc, prot = line.split('\t')
        bgc_prots[bgc].add(prot)

multi_nrps_bgcs = set([])
prots = set([])
for b in bgc_prots: 
    if len(bgc_prots[b]) > 1:
        multi_nrps_bgcs.add(b)
        for p in bgc_prots[b]:
            prots.add(p)

print('DATASET_HEATMAP')
print('SEPARATOR TAB')
print('DATASET_LABEL\tSame BGC')
print('COLOR\t#000000')
print('FIELD_LABELS\t' + '\t'.join(sorted(multi_nrps_bgcs)))
print('DATA')
for p in prots:
    plist = [p]
    for b in sorted(multi_nrps_bgcs):
        if p in bgc_prots[b]:
            plist.append('1')
        else:
            plist.append('0')
    print('\t'.join(plist))
