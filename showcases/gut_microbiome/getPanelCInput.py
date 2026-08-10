import os
import sys
from collections import defaultdict

slclust_dir = 'Slclust_OG_Listings/'
dom_dir = 'Domain_and_Interdomain_Coordinates/' # directory within bofasa prep results

protein_doms = defaultdict(set)
for f in os.listdir(dom_dir):
    dom_file = dom_dir + f 
    with open(dom_file) as odf:
        for i, line in enumerate(odf):
            if i == 0: continue
            line = line.strip('\n')
            ls = line.split()
            if ls[2] == 'inter-domain_region': continue
            protein_doms[ls[1]].add(ls[2])

print('method\tlarge_og_id\tproteins\ttot_avg_doms_ratio\ttot_doms\tavg_doms')
for f in os.listdir(slclust_dir):
    method = f.split('.txt')[0]
    slclust_file = slclust_dir + f
    with open(slclust_file) as osf:
        for i, line in enumerate(osf):
            line = line.strip('\n')
            ls = line.split()
            if len(ls) < 100: continue

            og_id = 'OG_' + str(i)

            union_doms = set([])
            pd_counts = []
            for p in ls:
                pds = protein_doms[p]
                union_doms = union_doms.union(pds)
                pd_counts.append(len(pds))

            tot_doms = len(union_doms)
            avg_dom_count = sum(pd_counts)/len(pd_counts)

            print(method + '\t' + og_id + '\t' + str(len(ls)) + '\t' + str(tot_doms/avg_dom_count) + '\t' + str(tot_doms) + '\t' + str(avg_dom_count))
            
