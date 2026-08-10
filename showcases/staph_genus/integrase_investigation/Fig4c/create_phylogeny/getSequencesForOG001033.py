import os
import sys
from Bio import SeqIO

bofa_file = '../Bofasa_Run_Emg_RS1000_Results/Final_Results/Protein_Ortholog_Groups.tsv'
prot_dir = '../Bofasa_Prep_Emg_Results/Genome_Processing/Proteomes/'

intg = set([])
with open(bofa_file) as obf:
    for line in obf:
        line = line.strip()
        ls = line.split('\t')
        if ls[0] == 'OG001033':
            for prots in ls[1:]:
                for p in prots.split(','):
                    p = p.strip()
                    intg.add(p)

for f in os.listdir(prot_dir):
    prot_file = prot_dir + f
    with open(prot_file) as opf:
        for rec in SeqIO.parse(opf, 'fasta'):
            if rec.id in intg:
                print('>' + rec.id + '\n' + str(rec.seq))
            
