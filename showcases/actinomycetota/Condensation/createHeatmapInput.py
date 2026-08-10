import os
import sys
from collections import defaultdict

species_order = []
with open('../Full_Species_Tree_Order.txt') as ostof:
    for line in ostof:
        line = line.strip()
        species_order.append(line)

adn_dogs = set([])
dog_order = {}
with open('Condensation_DOGs.txt') as oaf:
    for j, line in enumerate(oaf):
        line = line.strip()
        ls = line.split('\t')
        adn_dogs.add(ls[0])
        dog_order[ls[0]] = j

nrps_lts = set([])
with open('../NRPS_Locus_Tags.txt') as onlt:
    for line in onlt:
        line = line.strip()
        ls = line.split('\t')
        nrps_lts.add(ls[2])

samples = []
outf_heatmap = open('dog_heatmap_track.txt', 'w')
outf_dog_prop = open('dog_track.txt', 'w')

outf_heatmap.write('\t'.join(['dog', 'dog_order', 'species', 'species_order', 'count']) + '\n')
outf_dog_prop.write('\t'.join(['dog', 'color', 'dog_order', 'condensation_proportion', 'nrps_proportion', 'total_count']) + '\n')

with open('../Domain_Ortholog_Groups.tsv') as odf:
    for i, line in enumerate(odf):
        line = line.strip('\n')
        ls = line.split('\t')
        if i == 0: 
            samples = ls[1:]
        dog = ls[0]
        if not dog in adn_dogs: continue
        dog_samples = set([])
        adn_count = 0
        nrps_count = 0 
        tot_count = 0
        for j, doms in enumerate(ls[1:]):
            for dom in doms.split(', '):
                dom = dom.strip()
                if dom == '': continue
                s = samples[j]
                dog_samples.add(s)
                if 'Condensation' in dom:
                    adn_count += 1
                lt = dom.split('|')[1]
                if lt in nrps_lts:
                    nrps_count += 1
                tot_count += 1

        if len(dog_samples) >= 2:
            sample_dog_counts = defaultdict(int)
            for j, doms in enumerate(ls[1:]):
                doms = doms.strip()
                s = samples[j]
                if doms == '': continue
                for dom in doms.split(', '):
                    sample_dog_counts[s] += 1

            color = 'NA'
            if (adn_count/float(tot_count)) >= 0.5 and (nrps_count/float(tot_count)) >= 0.25 and tot_count >= 20:
                color = dog
                outf_dog_prop.write('\t'.join([dog, color, str(str(nrps_count/float(tot_count))), str(adn_count/float(tot_count)), str(nrps_count/float(tot_count)), str(tot_count)]) + '\n')

                for j, s in enumerate(species_order):
                    count = str(sample_dog_counts[s])
                    if count == '0':
                        count = 'NA'
                    
                    count_value = '0'
                    if sample_dog_counts[s] == 1:
                        count_value = '1'
                    elif sample_dog_counts[s] > 1:
                        count_value = '2'
                    outf_heatmap.write('\t'.join([dog, str(nrps_count/float(tot_count)), s, str(j), count_value]) + '\n')
            
outf_heatmap.close()
outf_dog_prop.close()
