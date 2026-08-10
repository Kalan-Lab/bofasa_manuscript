import os
import sys

freq_dir = 'OG_Summaries/'

method_name = {'kofam': 'KOfam', 'orthofinder_v2': 'OrthoFinder', 'orthofinder_v3': 'OrthoFinder', 'sonicparanoid': 'SonicParanoid', 'pirate': 'PIRATE', 'bofasa_emg_rs1000': 'bofasa', 'bofasa': 'bofasa', 'scarap': 'SCARAP'}

print('method\tmethod_name\tog\tsize')
for f in os.listdir(freq_dir):
    method = f.split('.txt')[0]
    
    with open(freq_dir + f) as off:
        for i, line in enumerate(off):
            if i == 0: continue
            line = line.strip()
            ls = line.split('\t')
            print(method + '\t' + method_name[method] + '\t' + ls[0] + '\t' + ls[1])
