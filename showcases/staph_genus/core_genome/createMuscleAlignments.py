import os
import sys
from Bio import SeqIO

scc_list_file = sys.argv[1]
method = scc_list_file.split('/')[-1].split('.')[0]
results_dir = os.path.abspath(sys.argv[2]) + '/'

method_prot_to_sccog = {}
with open(scc_list_file) as oslf:
    for i, line in enumerate(oslf):
        line = line.strip()
        ls = line.split()
        for p in ls:
            method_prot_to_sccog[p] = str(i)

prot_dir = os.path.abspath('../Bofasa_Prep_Results/Genome_Processing/Proteomes/') + '/'

for f in os.listdir(prot_dir):
    g = f.split('.faa')[0]
    with open(prot_dir + f) as opf:
        for rec in SeqIO.parse(opf, 'fasta'):
            if rec.id in method_prot_to_sccog:
                outf = open(results_dir + method_prot_to_sccog[rec.id] + '.faa', 'a+')
                outf.write('>' + g + '|'  + rec.id + '\n' + str(rec.seq) + '\n')
                outf.close()

for f in os.listdir(results_dir):
    if f.endswith('.faa') and not f.endswith('.msa.faa'):
        muscle_cmd = ['muscle', '-super5', results_dir + f + ' -threads', '1', '-output', results_dir + f.split('.')[0] + '.msa.faa'] 
        print(' '.join(muscle_cmd))
