import os
import sys

ogs = set(['OG006197', 'OG019627'])

bgc_prods = {}
with open('BGC_Types.txt') as obtf:
    for i, line in enumerate(obtf):
        if i == 0: continue
        line = line.strip()
        ls = line.split('\t')
        bgc_prods[ls[1]] = ls[-2] 

prot_to_bgc = {}
with open('NRPS_Locus_Tags.txt') as onltf:
    for line in onltf:
        line = line.strip()
        ls = line.split('\t')
        prot_to_bgc[ls[2]] = ls[1]

with open('Protein_Ortholog_Groups.tsv') as opogf:
    for line in opogf:
        line = line.strip('\n')
        ls = line.split('\t')
        if ls[0] in ogs:
            for ps in ls[1:]:
                for p in ps.split(', '):
                    if p.strip() == '': continue
                    if p in prot_to_bgc:
                        print(ls[0] + '\t' + p + '\t' + prot_to_bgc[p] + '\t' + bgc_prods[prot_to_bgc[p]])
                    else:
                        print(ls[0] + '\t' + p + '\tNA\tNA')
