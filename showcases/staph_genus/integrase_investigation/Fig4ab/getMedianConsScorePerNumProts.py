import os
import sys
from collections import defaultdict
import statistics
import numpy

prot_ranges_of_interest = [1, 10, 118, 12, 16, 17, 2, 3, 4, 5, 57, 59]

"""
0       OG
1       Median OG length (bp)
2       Percentage contexts near scaffold edge
3       Number of genomes with OG
4       Number of protein in OG
5       Single-copy
6       Context conservation score
7       Context conservation score - complete contexts
8       Number of distinct neighbor OGs
9       Number of distinct OGs from complete contexts
10      Avg. number of distinct neighbor OGs
11      Avg. number of distinct neighbor OGs from complete contexts
12      Percentage instances on plasmid (based on geNomad annotation)
13      Percentage instances on phage (based on geNomad annotation)
14      Percentage homologous to IS-elements (based on ISfinder database)
15      Instances
16      Contexts
"""

print('\t'.join(['num_prots', 'median', 'per10', 'per90']))
prot_num_ccs = defaultdict(list)
with open('../Bofasa_Run_Emg_RS1000_Results/Surrounding_Context_Information/OrthoGroup_Contexts.tsv') as of:
    for i, line in enumerate(of):
        if i == 0: continue
        line = line.strip()
        ls = line.split('\t')
        prots = int(ls[4])
        #if prots in prot_ranges_of_interest:
        ccs = float(ls[6])
        prot_num_ccs[prots].append(ccs)

for p in prot_num_ccs:
    ccss = prot_num_ccs[p]
    if len(ccss) >= 20:
        print(str(p) + '\t' + str(statistics.median(ccss)) + '\t' + str(numpy.percentile(ccss, 10)) + '\t' + (str(numpy.percentile(ccss, 90))))
