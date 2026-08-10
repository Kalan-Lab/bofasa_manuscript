import os
import sys

scc_dir = os.path.abspath('SCC_OG_Listings/') + '/'
cga_dir = os.path.abspath('CG_Alignments/') + '/'

for f in os.listdir(scc_dir):
    m = '.'.join(f.split('.')[:-1])
    outdir = cga_dir + m + '/'
    os.system('mkdir ' + outdir)
    os.system('python createMuscleAlignments.py ' + scc_dir + f + ' ' + outdir)
