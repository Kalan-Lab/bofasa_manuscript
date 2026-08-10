import os
import sys
from collections import defaultdict

pha_file = '../Bofasa_Prep_Results/Sample_Phage_Proteins.txt'
slclust_dir = 'Integrases_OG_Slclusters/'
int_dom_file = 'Integrase_Pfam_Domains.txt'
pro_dom_file = '../Bofasa_Prep_Results/Sample_Domain_and_InterDomain_Information.txt'

integrases = set([])
with open(int_dom_file) as oidf:
    for line in oidf:
        line = line.strip()
        ls = line.split()
        integrases.add(ls[1])

prot_integrases = set([])
with open(pro_dom_file) as opdf:
    for line in opdf:
        line = line.strip()
        ls = line.split('\t')
        if ls[2] in integrases:
            prot_integrases.add(ls[1])

phage_proteins = set([])
with open(pha_file) as opf:
    for line in opf:
        line = line.strip()
        ls = line.split('\t')
        phage_proteins.add(ls[1])

print('method\tog\tog_tot_prots\tcat\tcount')
for f in os.listdir(slclust_dir):
    method = f.split('.txt')[0]
    
    integrases_clustered = set([])
    with open(slclust_dir + f) as osf:
        for i, line in enumerate(osf):
            line = line.strip('\n')
            ls = line.split()
            prot_num = len(ls)
            og = method + '|OG_' + str(i)
            for p in ls:
                integrases_clustered.add(p)
            print('\t'.join([method, og, str(prot_num), 'phage', str(len(set(ls).intersection(phage_proteins)))]))
            print('\t'.join([method, og, str(prot_num), 'other', str(len(set(ls).difference(phage_proteins)))]))

    singletons = 0
    singletons_phage = 0
    singletons_other = 0 
    for p in prot_integrases:
        if not p in integrases_clustered:
            singletons += 1
            if p in phage_proteins:
                singletons_phage += 1
            else:
                singletons_other += 1 

    if singletons > 0:
        print('\t'.join([method, method + '|singletons', str(singletons), 'singletons', str(singletons)]))
