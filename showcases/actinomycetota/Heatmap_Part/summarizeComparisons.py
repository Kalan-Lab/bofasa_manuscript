import os
import sys

og_list_dir = os.path.abspath('OG_Listings') + "/"
scc_og_list_dir = os.path.abspath('SCC_OG_Listings') + "/"
pw_comp_dir = os.path.abspath('Pairwise_Comparisons') + "/"

op_counts = {}
for f in os.listdir(og_list_dir):
    method = f.split('.txt')[0]
    count = 0
    with open(og_list_dir + f) as olf:
        for line in olf:
            count += 1
    op_counts[method] = count

scc_op_counts = {}
for f in os.listdir(scc_og_list_dir):
    method = f.split('.txt')[0]
    count = 0 
    with open(scc_og_list_dir + f) as oslf:
        for line in oslf:
            count += 1
    scc_op_counts[method] = count

print('\t'.join(['method1', 'method2', 'overlap', 'm1_total_op', 'm1_scc_op']))
for f in os.listdir(pw_comp_dir):
    m1 = f.split('_vs_')[0]
    m2 = f.split('_vs_')[1].split('.txt')[0]
    with open(pw_comp_dir + f) as opf:
        for i, line in enumerate(opf):
            if i == 0: continue
            line = line.strip()
            ls = line.split('\t')
            intersect = int(ls[-2])
    overlap_m1 = intersect/float(op_counts[m1])
    overlap_m2 = intersect/float(op_counts[m2])
    print('\t'.join([m1, m2, str(overlap_m1), str(op_counts[m1]), str(scc_op_counts[m1])]))
    print('\t'.join([m2, m1, str(overlap_m2), str(op_counts[m2]), str(scc_op_counts[m2])]))
