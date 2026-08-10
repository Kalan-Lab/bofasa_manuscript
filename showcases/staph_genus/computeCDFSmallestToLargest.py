import os
import sys
from collections import defaultdict

sum_dir = 'OG_Summaries/'

method_to_name = {'bofasa': 'bofasa\t1', 'bofasa_rs1000': 'bofasa\t2', 'bofasa_emg_rs1000': 'bofasa\t2', 'sonicparanoid_default': 'SonicParanoid\t1', 'sonicparanoid_sensitive': 'SonicParanoid\t2', 'orthofinder_v2': 'OrthoFinder\t1', 'orthofinder_v3': 'OrthoFinder\t2', 'pirate': 'PIRATE\t1', 'pirate_moresteps': 'PIRATE\t2', 'scarap': 'SCARAP\t1'}
print('method\ttype\tindex\tcdf\tog_size')
for f in os.listdir(sum_dir): 
    og_sizes = []
    with open(sum_dir + f) as osf:
        for line in osf:
            line = line.strip()
            ls = line.split('\t')
            og_sizes.append(int(ls[1]))
    
    method = f.split('.')[0]
    method_name = method_to_name[method]
    total = 0
    print(method_name + '\t0\t0\tNA') 
    for i, ogs in enumerate(sorted(og_sizes, reverse=False)):
        total += ogs
        print(method_name + '\t' + str(i+1) + '\t' + str(total) + '\t' + str(ogs))
