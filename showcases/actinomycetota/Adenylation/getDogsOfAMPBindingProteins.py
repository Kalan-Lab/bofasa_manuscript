import os
import sys

with open('../Domain_Ortholog_Groups.tsv') as odf:
    for i, line in enumerate(odf):
        line = line.strip('\n')
        ls = line.split('\t')
        if i == 0: continue
        dog = ls[0]
        adn_count = 0
        tot_count = 0
        for doms in ls[1:]:
            for dom in doms.split(', '):
                dom = dom.strip()
                if dom == '': continue
                if '|AMP-binding|' in dom:
                    adn_count += 1
                tot_count += 1
        if adn_count > 0:
            print(dog + '\t' + str(adn_count) + '\t' + str(adn_count/float(tot_count)))
