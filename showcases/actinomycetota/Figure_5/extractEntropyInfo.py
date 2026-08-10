import os
import sys

bofasa = set([])
with open('Scatterplot_Input.txt') as obf:
    for line in obf:
        line = line.strip()
        ls = line.split('\t')
        if ls[0] == 'bofasa':
            bofasa.add(ls[1])

with open('OrthoGroup_Contexts.tsv') as of:
    for i, line in enumerate(of):
        line = line.strip('\n')
        ls = line.split('\t')
        keep_line = '\t'.join(ls[:-2])
        if i == 0 or ls[0] in bofasa:
            print(keep_line)

