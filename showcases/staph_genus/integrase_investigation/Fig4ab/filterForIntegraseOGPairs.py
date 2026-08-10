import os
import sys
from collections import defaultdict

intg_file = 'Integrases_by_Association_Methods.txt'
og_list_dir = 'OG_Listings/'
intg_og_list_dir = 'Integrases_OG_Listings/'
intg_og_slclust_dir = 'Integrases_OG_Slclusters/'

method_integrases = defaultdict(set)
with open(intg_file) as oif:
    for line in oif:
        line = line.strip()
        ls = line.split('\t')
        method_integrases[ls[0]].add(ls[1])

for f in os.listdir(og_list_dir):
    method = f.split('.')[0]
    og_list_file = og_list_dir + f
    out_file = open(intg_og_list_dir + f, 'w') 
    with open(og_list_file) as oolf:
        for line in oolf:
            line = line.strip()
            ls = line.split('\t')
            if ls[0] in method_integrases[method] or ls[1] in method_integrases[method]:
                out_file.write(line + '\n')
    out_file.close()

for f in os.listdir(intg_og_list_dir):
    inf = intg_og_list_dir + f 
    slf = intg_og_slclust_dir + f
    os.system('slclust < ' + inf + ' > ' + slf)
