import os
import sys
from collections import defaultdict
from Bio import SeqIO

focal_og_file = sys.argv[1]
nrps_lt_file = 'NRPS_Locus_Tags.txt'
antismash_dir = 'antiSMASH/AntiSMASH_Results/'
prot_og_file = 'Protein_Ortholog_Groups.tsv'

tp_det_file = 'Crits-Christoph_hmmdetails.txt'
tp_res_file = 'Transcporter_Search_Results.txt'
mp_det_file = 'Reitz_hmmdetails.txt'
mp_res_file = 'Metallophore_Search_Results.txt'

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

tp_pfs = set([])
mp_pfs = set([])
hmm_cuts = defaultdict(lambda: None)
with open(tp_det_file) as otdf:
    for line in otdf:
        line = line.strip('\n')
        ls = line.split('\t')
        hmm_cuts[ls[0]] = float(ls[2])
        tp_pfs.add(ls[0])

with open(mp_det_file) as omdf:
    for line in omdf:
        line = line.strip('\n')
        ls = line.split('\t')
        hmm_cuts[ls[0]] = float(ls[2])
        if ls[0] == 'FbnE': continue # no cutoff in hmmdetails file
        mp_pfs.add(ls[0])

tp_bits = defaultdict(lambda: defaultdict(lambda: 0.0))
mp_bits = defaultdict(lambda: defaultdict(lambda: 0.0))
with open(tp_res_file) as otrf:
    for line in otrf:
        line = line.strip('\n')
        ls = line.split('\t')
        # Cy_tandem       KCDDEKNF_03286  349.0616760253906       94.64146423339844
        norm_dom_score = float(ls[-1])/hmm_cuts[ls[0]]
        if norm_dom_score > tp_bits[ls[1]][ls[0]]:
            tp_bits[ls[1]][ls[0]] = norm_dom_score

with open(mp_res_file) as omrf:
    for line in omrf:
        line = line.strip('\n')
        ls = line.split('\t')
        # Cy_tandem       KCDDEKNF_03286  349.0616760253906       94.64146423339844
        if ls[0] == 'FbnE': continue # no cutoff in hmmdetails file
        norm_dom_score = float(ls[-1])/hmm_cuts[ls[0]]
        if norm_dom_score > mp_bits[ls[1]][ls[0]]:
            mp_bits[ls[1]][ls[0]] = norm_dom_score

bgc_to_ltp = {}
bgc_tp_bits = defaultdict(lambda: defaultdict(lambda: 0.0))
bgc_mp_bits = defaultdict(lambda: defaultdict(lambda: 0.0))
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
                        lt = feat.qualifiers.get('locus_tag')[0]
                        ltp = lt.split('_')[0]
                        bgc_to_ltp[bgc] = ltp

                        for pf in tp_pfs:
                            bss = tp_bits[lt][pf]
                            if bss > bgc_tp_bits[bgc][pf]:
                                bgc_tp_bits[bgc][pf] = bss

                        for pf in mp_pfs:
                            bss = mp_bits[lt][pf]
                            if bss > bgc_mp_bits[bgc][pf]:
                                bgc_mp_bits[bgc][pf] = bss

focal_og = focal_og_file.split('.txt')[0]
print('\t'.join(['focal_og', 'bgc_id', 'profile', 'category', 'best_standardized_score']))
for s in os.listdir(antismash_dir):
    sample_dir = antismash_dir + s + '/'
    for f in os.listdir(sample_dir):
        if not 'region' in f or not f.endswith('.gbk'): continue
        bgc = f.split('.gbk')[0]
        if not bgc in bgc_to_ltp: continue 
        ltp = bgc_to_ltp[bgc]
        order = lt_to_order[ltp]
        ord_str = str(order)
        if len(ord_str) == 1:
            ord_str = '0' + ord_str        
        if bgc == 'CP002040.1.region002':
            ord_str = '07'

        for pf in tp_pfs:
            bss = bgc_tp_bits[bgc][pf]
            print('\t'.join([focal_og, ord_str + '. ' + bgc, pf, 'transporter', str(bss)]))

        for pf in mp_pfs:
            bss = bgc_mp_bits[bgc][pf]
            print('\t'.join([focal_og, ord_str + '. ' + bgc, pf, 'metallophore', str(bss)]))

