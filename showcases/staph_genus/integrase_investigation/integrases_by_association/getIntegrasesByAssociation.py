import os
import sys
from collections import defaultdict

int_dom_file = 'Integrase_Pfam_Domains.txt'
pro_dom_file = '../Bofasa_Prep_Results/Sample_Domain_and_InterDomain_Information.txt'
og_listing_dir = os.path.abspath('OG_Listings/') + '/'

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

for f in os.listdir(og_listing_dir):
    method = f.split('.txt')[0]
    select = set([])
    with open(og_listing_dir + f) as olf:
        for line in olf:
            line = line.strip()
            ls = line.split('\t')
            if ls[0] in prot_integrases or ls[1] in prot_integrases:
                select.add(ls[0])
                select.add(ls[1])

    for p in prot_integrases:
        if not p in select:
            print(method + '\t' + p)
    for p in select:
        print(method + '\t' + p)
