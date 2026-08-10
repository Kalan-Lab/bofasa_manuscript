import os
import sys

og_list_dir = os.path.abspath(sys.argv[1]) + '/'
comp_dir = os.path.abspath(sys.argv[2]) + '/'

og_files = {}
for f in os.listdir(og_list_dir):
    n = f.split('.')[0]
    og_files[n] = og_list_dir + f
    
for i, n1 in enumerate(sorted(og_files)):
    for j, n2 in enumerate(sorted(og_files)):
        if i >= j: continue
        outf = comp_dir + n1 + '_vs_' + n2 + '.txt'
        f1 = og_files[n1]
        f2 = og_files[n2]
        cmd = ['compare_og_pairs.py', '-a', f1, '-b', f2, '>', outf]
        print(' '.join(cmd))
