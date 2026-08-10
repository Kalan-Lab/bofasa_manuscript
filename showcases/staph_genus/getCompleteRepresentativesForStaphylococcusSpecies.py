import os
import sys
from collections import defaultdict
from operator import itemgetter
import statistics

staph_species_comp_assemblies = defaultdict(list)
with open('bac120_metadata_r226.tsv') as ogf:
    for i, line in enumerate(ogf):
        if i == 0: continue
        line = line.strip()
        ls = line.split('\t')
        if not ';s__' in ls[19]: continue
        sp = ls[19].split(';s__')[1].split(';')[0]
        if not sp.startswith('Staphylococcus'): continue
        gca = ls[57]
        n50 = float(ls[47]) # n50_scaffolds
        assembly_level = ls[48]
        if assembly_level == 'Complete Genome':
            staph_species_comp_assemblies[sp].append([gca, n50])

# I had difficulities downloading the following genomes, potentially 
# because they might have retrospectively been suppressed by the 
# authors. 
bad_gcas = set(['GCA_033597815.2', 'GCA_039237145.1', 'GCA_039234925.1'])
for sp in staph_species_comp_assemblies:
    median_n50 = statistics.median([x[1] for x in staph_species_comp_assemblies[sp]])

    best_gca = None
    best_stat = 1e100
    for gen in staph_species_comp_assemblies[sp]:
        if gen[0] in bad_gcas: continue
        stat = abs(median_n50 - gen[1])
        if stat < best_stat:
            best_gca = gen[0]
            best_stat = stat
    if best_gca != None:
        print(sp + '\t' + best_gca)
