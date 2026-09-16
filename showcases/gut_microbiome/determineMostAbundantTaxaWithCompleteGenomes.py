import os
import sys
from collections import defaultdict
from Bio import SeqIO
import statistics
from operator import itemgetter
import random

gtdb_results_file = 'prepare_dataset/GTDB_R226_Results/gtdbtk.bac120.summary.tsv'
rel_abd_file = 'prepare_dataset/Files_from_Eitan/bins_abundance.txt'
gtdb_meta_file = 'bac120_metadata_r226.tsv'

mgb_taxon = {}
with open(gtdb_results_file) as ogrf:
    for i, line in enumerate(ogrf):
        if i == 0: continue
        line = line.strip()
        ls = line.split('\t')
        taxon = ls[1]
        mgb = ls[0]
        mgb_taxon[mgb] = taxon

taxon_rel_abds = defaultdict(list)
with open(rel_abd_file) as oraf:
    for line in oraf:
        if i == 0: continue
        line = line.strip()
        ls = line.split('\t')
        mgb = ls[2]
        if mgb in mgb_taxon:
            taxon = mgb_taxon[mgb]
            for hra in ls[3:7]:
                hra = float(hra)
                taxon_rel_abds[taxon].append(hra)

taxon_med_abds = {}
for taxon in taxon_rel_abds:
    median_rel_abd = statistics.median(taxon_rel_abds[taxon])
    taxon_med_abds[taxon] = median_rel_abd

bad = set(['d__Bacteria;p__Actinomycetota;c__Coriobacteriia;o__Coriobacteriales;f__Eggerthellaceae;g__Adlercreutzia;s__Adlercreutzia rubneri'])
complete_genomes = defaultdict(set)
with open(gtdb_meta_file) as ogmf:
    for i, line in enumerate(ogmf):
        if i == 0: continue
        line = line.strip()
        ls = line.split('\t')
        gca = ls[57]
        level = ls[48]
        taxon = ls[19]
        if level == 'Complete Genome':
            complete_genomes[taxon].add(gca)

selected = 1
for taxon in sorted(taxon_med_abds.items(), key=itemgetter(1), reverse=True):
    if selected > 100: break
    if (taxon[0] not in complete_genomes) or (taxon[0] in bad): continue
    species = taxon[0].split(';s__')[1]
    if species.strip() == '': continue
    print(str(selected) + '\t' + taxon[0] + '\t' + str(random.choice(list(complete_genomes[taxon[0]]))))
    selected += 1

