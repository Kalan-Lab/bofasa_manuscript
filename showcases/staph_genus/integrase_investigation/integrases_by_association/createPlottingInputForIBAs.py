import os
import sys
from collections import defaultdict

"""
protein
bofasa_emg_OG
domain_architecture
genomad_context
method_count
methods
found_by_bofasa_emg
call_on_whether_recombinase_or_integrase
notes
"""

iba_file = 'Integrase_by_Association_Info.txt'
method_cat_counts = defaultdict(lambda: defaultdict(int))

#print('protein\tmethod\tcall\tmethod_support')
#print('method\tcategory\tcount')
print('protein\tcall\tmethod_support')
with open(iba_file) as oif:
    for i, line in enumerate(oif):
        if i < 2: continue
        line = line.strip('\n')
        ls = line.split('\t')
        methods = ls[5]
        for m in methods.split('; '):
            m = m.strip()
            #print(ls[0] + '\t' + m + '\t' + ls[-2] + '\t' + ls[4])
            method_cat_counts[m][ls[-2]] += 1
            print(ls[0] + '\t' + ls[-2] + '\t' + ls[4])
#for m in method_cat_counts:
#    for c in method_cat_counts[m]:
#        print(m + '\t' + c + '\t' + str(method_cat_counts[m][c]))
