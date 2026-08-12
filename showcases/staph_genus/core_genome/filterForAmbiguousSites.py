import os
import sys
from Bio import SeqIO

seqs = []
for rec in SeqIO.parse(sys.argv[1], 'fasta'):
    seqs.append([rec.description] + list(str(rec.seq)))

seqs_filt = []
for i, pos in enumerate(zip(*seqs)):
    if i == 0: 
        seqs_filt.append(list(pos))
    else:
        gappy = 0
        total = 0
        for al in list(pos):
            total += 1
            if al == '-' or al.upper() == 'X':
                gappy += 1

        gappy_prop = gappy/float(total)
        if gappy_prop < 0.1:
            seqs_filt.append(list(pos))

for seq in zip(*seqs_filt):
    seqstring = ''.join(seq[1:])
    if len(seqstring) > 0:
        gappy = 0
        total = 0
        for al in str(seqstring):
            if al == '-' or al.upper() == 'X':
                gappy += 1
            total += 1
        gappy_prop = gappy/float(total)
        if gappy_prop < 0.1:
            print('>' + seq[0] + '\n' + seqstring)
