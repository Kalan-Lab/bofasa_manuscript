import os
import sys

int_og_file = 'Bofasa_Emg_RS1000_Integrase_OGs.txt'

intg_ogs = set([])
with open(int_og_file) as oiof:
    for line in oiof:
        intg_ogs.add(line.strip())

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

sa_file = '../Bofasa_Run_Emg_RS1000_Results/Surrounding_Context_Information/OrthoGroup_Contexts.tsv'

print('og\tnum_prots\tcontext_conservation_score\tphage_context')
with open(sa_file) as osf:
    for i, line in enumerate(osf):
        if i == 0: continue
        line = line.strip('\n')
        ls = line.split('\t')
        og = ls[0]
        per_phage = float(ls[13])
        phage_context = 'False'
        if per_phage >= 50.0:
            phage_context = 'True'

        og = ls[0]
        num_prots = ls[4]
        ccs = ls[6]
        if og in intg_ogs:
            print(og + '\t' + num_prots + '\t' + ccs + '\t' + phage_context)
