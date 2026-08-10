import os
import sys
from collections import defaultdict
from Bio import SeqIO

nrps_prot_file = 'NRPS_Locus_Tags.txt'
adn_file = '../Adenylation/dog_track.txt'
con_file = '../Condensation/dog_track.txt'
dog_mat_file = 'Domain_Ortholog_Groups.tsv'
dog_coord_file = 'Sample_Domain_and_InterDomain_Information.txt'
prot_dir = '../../Bofasa_Prep_Prokka/Genome_Processing/Proteomes/'

prot_lengths = {}
for f in os.listdir(prot_dir):
    with open(prot_dir + f) as opf:
        for rec in SeqIO.parse(opf, 'fasta'):
            prot_lengths[rec.id] = str(len(rec.seq))

dom_to_dog = {}
with open(dog_mat_file) as odmf:
    for i, line in enumerate(odmf):
        line = line.strip('\n')
        ls = line.split('\t')
        if i == 0: continue
        dog = ls[0]
        for doms in ls[1:]:
            for dom in doms.split(','):
                if dom.strip() != '':
                    dom_to_dog[dom.strip()] = dog

nrps_lts = set([])
with open(nrps_prot_file) as onpf:
    for line in onpf:
        line = line.strip()
        ls = line.split('\t')
        nrps_lts.add(ls[-1])

all_adn_dogs = set([])
all_con_dogs = set([])
with open(adn_file) as oaf:
    for line in oaf:
        line = line.strip()
        ls = line.split('\t')
        dog = ls[0]
        all_adn_dogs.add(dog)

with open(con_file) as ocf:
    for line in ocf:
        line = line.strip()
        ls = line.split('\t')
        dog = ls[0]
        all_con_dogs.add(dog)

adn_dog_cols = {"OG0000028_5": "#D5E3EF", "OG0000028_13": "#C6D8E9", "OG0000028_3": "#B7CDE3", "OG0000028_14": "#A9C3DE", "OG0000028_38": "#9CB7D7", "OG0000028_21": "#94A6CE", "OG0000028_30": "#8C96C6", "OG0000028_2": "#8C82BC", "OG0000028_23": "#8C6FB3", "OG0000028_31": "#8A5DAA", "OG0000028_0": "#884AA1", "OG0000028_4": "#863595", "OG0000028_6": "#831F87", "OG0000028_7": "#7B0D76", "OG0000028_56": "#640660", "OG0000028_57": "#4D004B"}
con_dog_cols = colors = {"OG0000054_8": "#E8F6AE", "OG0000054_31": "#D9F0A3", "OG0000054_36": "#C3E698", "OG0000054_2": "#ADDD8E", "OG0000054_0": "#92D183", "OG0000054_56": "#78C679", "OG0000054_6": "#5CB86A", "OG0000054_7": "#41AB5D", "OG0000054_9": "#329750", "OG0000054_26": "#238443", "OG0000054_32": "#11763D", "OG0000790_0": "#006837", "OG0000790_1": "#005630", "OG0000790_3": "#004529"}

protein_domains = defaultdict(list)
with open(dog_coord_file) as odcf:
    for i, line in enumerate(odcf):
        line = line.strip()
        gca, prot, dom, dom_id, start, end = line.split('\t')
        if prot not in nrps_lts: continue
        dom_name = '|'.join([gca, prot, dom, dom_id])
        # SHAPE|START|END|COLOR|LABEL
        prot_info = None
        if dom == 'full_protein':
            prot_info = ['RE', start, end, '#000000', 'full_protein']
        elif dom == 'Condensation':
            dog_og = dom_to_dog[dom_name]
            prot_info = ['TR', start, end, '#9c9b9a', dog_og]#'other']
            if dog_og in all_con_dogs:
                dog_col = con_dog_cols[dog_og] 
                prot_info = ['TR', start, end, dog_col, dog_og] 
        elif dom == 'AMP-binding':
            dog_og = dom_to_dog[dom_name]
            prot_info = ['EL', start, end, '#9c9b9a', dog_og]#'other']
            if dog_og in all_adn_dogs:
                dog_col = adn_dog_cols[dog_og]
                prot_info = ['EL', start, end, dog_col, dog_og]
        elif dom != 'inter-domain_region':
            dog_og = dom_to_dog[dom_name]
            prot_info = ['RE', start, end, '#9c9b9a', dog_og]#'inter-domain_region']
        if prot_info != None:
            protein_domains[prot].append('|'.join(prot_info))

print('DATASET_DOMAINS')
print('SEPARATOR TAB')
print('DATASET_LABEL\tDomains')
print('COLOR\t#000000')
print('DATA')

for p in protein_domains:
    doms = '\t'.join(protein_domains[p])
    print(p + '\t' + str(prot_lengths[p]) + '\t' + doms)
