import os
import sys
from collections import defaultdict

method_cat = defaultdict(lambda: defaultdict(int))
with open('Plotting_Input.txt') as opif:
    for i, line in enumerate(opif):
        if i == 0: continue
        line = line.strip('\n')
        ls = line.split('\t')
        if ls[0] == 'supergappy':
            method = ls[1]
            cat = ls[2]
            method_cat[method][cat] = int(ls[3])

oglist_dir = 'OG_Listings/'
og_pairs = defaultdict(int)
for f in os.listdir(oglist_dir):
    method = f.split('.txt')[0]
    with open(oglist_dir + f) as oof:
        for line in oof:
            line = line.strip('\n')
            og_pairs[method] += 1

print('gappy_cat\tmethod\tintersection_proportion\tgappy_specific_og_pairs')
for method in method_cat:
    comp = method_cat[method]['Complete-specific']
    gapp = method_cat[method]['Gappy-specific']
    inter = method_cat[method]['Intersection']

    inter_prop = inter/og_pairs[method]
    print('supergappy\t' + method + '\t' + str(inter_prop) + '\t' + str(gapp))
