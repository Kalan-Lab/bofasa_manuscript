import os
import sys
from collections import defaultdict
from Bio import SeqIO

scc_align_dir = 'CG_Alignments_Filtered_for_High_Ambiguous_Sites/'
print('method\talignment_length\tgap_proportion')
for m in os.listdir(scc_align_dir):
    mdir = scc_align_dir + m + '/'
    align_len = 0
    total = 0
    gap = 0
    for f in os.listdir(mdir):
        if not f.endswith('.msa.faa'): continue
        with open(mdir + f) as omf:
            for i, rec in enumerate(SeqIO.parse(omf, 'fasta')):
                sl = len(str(rec.seq))
                if i == 0: 
                    align_len += sl
                total += sl     
                for b in str(rec.seq):
                    if b == '-':
                        gap += 1
                
    if total == 0: continue
    gap_prop = gap/total

    print(m + '\t' + str(align_len) + '\t' + str(gap_prop) + '\t' + str(total-gap))
