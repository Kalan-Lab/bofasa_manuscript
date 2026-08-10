import os
import sys

with open('../Domain_Ortholog_Groups.tsv') as odf:
    for i, line in enumerate(odf):
        line = line.strip('\n')
        ls = line.split('\t')
        if i == 0: continue
        dog = ls[0]
        con_count = 0
        tot_count = 0
        for doms in ls[1:]:
            for dom in doms.split(', '):
                dom = dom.strip()
                if dom == '': continue
                if '|Condensation|' in dom:
                    con_count += 1
                tot_count += 1
        if con_count > 0:
            print(dog + '\t' + str(con_count) + '\t' + str(con_count/float(tot_count)))


