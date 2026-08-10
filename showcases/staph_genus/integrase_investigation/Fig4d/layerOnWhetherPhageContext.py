import os
import sys
from ete3 import Tree

phage_prots = set([])
with open('../Bofasa_Prep_Emg_Results/Sample_Phage_Proteins.txt') as obrf:
    for i, line in enumerate(obrf):
        phage_prots.add(line.strip().split('\t')[1])

t = Tree('OG001033.trimal_strict.msa.tre') 

print('DATASET_COLORSTRIP')
print('SEPARATOR TAB')
print('DATASET_LABEL\tPhage context')
print('COLOR\t#000000')
print('DATA')

for n in t.traverse('postorder'):
    if n.is_leaf():
        if n.name in phage_prots:
            print(n.name + '\t\tphage_context')
        else:
            print(n.name = '\t\tnon-phage_context')
