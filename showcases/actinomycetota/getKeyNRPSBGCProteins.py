import os
import sys
from Bio import SeqIO

antismash_dir = 'AntiSMASH_Results/'

for s in os.listdir(antismash_dir):
    samp_dir = antismash_dir + s + '/'
    s = '.'.join(s.split('.')[:-1])
    for f in os.listdir(samp_dir):
        if f.endswith('.gbk') and '.region' in f:
            gbk_file = samp_dir + f 
            with open(gbk_file) as ogf:
                for rec in SeqIO.parse(ogf, 'genbank'):
                    for feat in rec.features:
                        if feat.type == 'CDS':
                            try:
                                for gf in feat.qualifiers.get('gene_functions'):
                                    if 'rule-based-clusters' in gf and 'NRPS: AMP-binding' in gf:
                                        print(s + '\t' + f.split('.gbk')[0] + '\t' + feat.qualifiers.get('locus_tag')[0])
                            except: pass
