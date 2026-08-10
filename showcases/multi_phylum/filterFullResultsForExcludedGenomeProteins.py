import os
import sys

og_indir = '../small_multi_phyla/OG_Listings/'
og_outdir = 'Full_OG_Listings_without_Excluded_Genome/'

#scc_indir = '../small_multi_phyla/SCC_OG_Listings/'
#scc_outdir = 'Full_SCC_OG_Listings_without_Excluded_Genome/'

for f in os.listdir(og_indir):
    with open(og_outdir + f, 'w') as outf:
        with open(og_indir + f) as of:
            for line in of:
                if 'KCBHFKDJ' in line: continue
                outf.write(line)

"""
for f in os.listdir(scc_indir):
    with open(scc_outdir + f, 'w') as outf:
        with open(scc_indir + f) as of:
            for line in of:
                line = line.strip()
                ls = line.split()
                ls_filt = []
                for item in ls:
                    if 'KCBHFKDJ' in item:
                        ls_filt.append(item)
                outf.write('\t'.join(ls_filt) + '\n')
"""
