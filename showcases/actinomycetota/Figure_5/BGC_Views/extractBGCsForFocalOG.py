import os
import sys
from Bio import SeqIO
from collections import defaultdict

focal_og_file = sys.argv[1]
nrps_lt_file = 'NRPS_Locus_Tags.txt'
antismash_dir = 'antiSMASH/AntiSMASH_Results/'
prot_og_file = 'Protein_Ortholog_Groups.tsv'

pt_to_og = {}
with open(prot_og_file) as opf:
    for i, line in enumerate(opf):
        if i == 0: continue
        line = line.strip('\n')
        ls = line.split('\t')
        og = ls[0]
        for pts in ls[1:]:
            for pt in pts.split(','):
                pt = pt.strip()
                if pt == '': continue
                pt_to_og[pt] = og

select_nrps = set([])
lt_to_order = {}
with open(focal_og_file) as ogf:
    for i, line in enumerate(ogf):
        line = line.strip('\n')
        select_nrps.add(line)
        lt = line.split('_')[0]
        lt_to_order[lt] = i

select_bgcs = set([])
with open(nrps_lt_file) as onf:
    for line in onf:
        line = line.strip('\n')
        ls = line.split('\t')
        if ls[2] in select_nrps:
            select_bgcs.add(ls[1])

og_bgcs = defaultdict(set)
for s in os.listdir(antismash_dir):
    sample_dir = antismash_dir + s + '/'
    for f in os.listdir(sample_dir):
        if not 'region' in f or not f.endswith('.gbk'): continue
        bgc = f.split('.gbk')[0]
        bgc_file = sample_dir + f
        if bgc in select_bgcs:
            with open(bgc_file) as obf:
                for rec in SeqIO.parse(bgc_file, 'genbank'):
                    for feat in rec.features:
                        if feat.type != 'CDS': continue
                        start = feat.location.start
                        end = feat.location.end
                        lt = feat.qualifiers.get('locus_tag')[0]
                        og = pt_to_og[lt]
                        og_bgcs[og].add(bgc)

multi_bgc_ogs = set([])
for og in og_bgcs:
    if len(og_bgcs[og]) >= 5: 
        multi_bgc_ogs.add(og)

"""
      6 OG000192
      8 OG006062
      5 OG006067
      6 OG006068
      5 OG006184
     10 OG006196
     10 OG006197
      5 OG006198
      5 OG006922


      5 OG012569
      9 OG012852
      9 OG012853
      5 OG014458
      5 OG014936
      9 OG016096
      8 OG018362
      7 OG019626
     13 OG019627
"""


print('\t'.join(['locus_tag', 'ortholog_group', 'bgc_id', 'scaffold_id', 'start', 'end']))
for s in os.listdir(antismash_dir):
    sample_dir = antismash_dir + s + '/'
    for f in os.listdir(sample_dir):
        if not 'region' in f or not f.endswith('.gbk'): continue
        bgc = f.split('.gbk')[0]
        bgc_file = sample_dir + f
        if bgc in select_bgcs:
            with open(bgc_file) as obf:
                for rec in SeqIO.parse(bgc_file, 'genbank'):
                    for feat in rec.features:
                        if feat.type != 'CDS': continue
                        start = feat.location.start
                        end = feat.location.end
                        lt = feat.qualifiers.get('locus_tag')[0]
                        og = pt_to_og[lt]
                        name_og = 'Other'
                        if og in multi_bgc_ogs:
                            name_og = og
                        ltp = lt.split('_')[0]
                        order = lt_to_order[ltp]
                        ord_str = str(order)
                        if len(ord_str) == 1:
                            ord_str = '0' + ord_str
                        print('\t'.join([lt, name_og, ord_str + '. ' + bgc, rec.id, str(start), str(end)]))
