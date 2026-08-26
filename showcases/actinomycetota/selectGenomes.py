import os
import sys
from collections import defaultdict
from operator import itemgetter

gtdb_r214_tsv = 'bac120_metadata_r220.tsv'

assembly_level_values = {'Complete Genome': 4}

genus_comp_assemblies = defaultdict(list)
with open(gtdb_r214_tsv) as ogrt:
    for i, line in enumerate(ogrt):
        line = line.strip()
        ls = line.split('\t')
        if i == 0: continue 
        tax = ls[19]
        phylum = tax.split('p__')[1].split(';c__')[0]
        genus = tax.split(';g__')[1].split(';s__')[0]
        species = tax.split(';s__')[-1]
        tclass = tax.split(';c__')[1].split(';o__')[0]
        if phylum != 'Actinomycetota': continue 
        n50 = int(ls[46])
        gca = ls[57]
        assembly_level = ls[48]
        if assembly_level != 'Complete Genome': continue
        genus_comp_assemblies[genus].append([gca, n50])

for g in genus_comp_assemblies:
    for i, a in enumerate(sorted(genus_comp_assemblies[g], key=itemgetter(1), reverse=False)):
        if i == 0 and a[1] >= 5000000:
            print(g + '\t' + a[0] + '\t' + str(a[1]))
