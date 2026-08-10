import os
import sys
from Bio import SeqIO

focal_og_file = sys.argv[1]
in_dir = 'antiSMASH/AntiSMASH_Results/'
bed_dir = 'BEDs/'
res_dir = 'BGC_Regions_Strict_Window_Bounds/'


select_nrps = set([])
with open(focal_og_file) as ogf:
    for i, line in enumerate(ogf):
        line = line.strip('\n')
        select_nrps.add(line)

select_nrps_coords = {}
for f in os.listdir(bed_dir):
    with open(bed_dir + f) as obf:
        for line in obf:
            line = line.strip('\n')
            ls = line.split('\t')
            lt = ls[3] 
            if lt in select_nrps:
                select_nrps_coords[lt] = ls[:3]

for s in os.listdir(in_dir):
    full_genome_gbk = in_dir + s + '/' + s
    print(full_genome_gbk)
    assert(os.path.isfile(full_genome_gbk))

    samp_dir = res_dir + s + '/'
    if not os.path.isdir(samp_dir):
        os.system('mkdir ' + samp_dir)
    
    with open(full_genome_gbk) as ofgg:
        for rec in SeqIO.parse(ofgg, 'genbank'):
            for feat in rec.features:
                if feat.type != 'CDS': continue
                lt = feat.qualifiers.get('locus_tag')[0]
                if lt in select_nrps:
                    start = feat.location.start
                    end = feat.location.end
                    region_start = start - 20000
                    region_stop = end + 20000
                
                    annotations = rec.annotations.copy()
                    lt_context = rec[region_start:region_stop]
                    lt_context.annotations = annotations
    
                    of = open(samp_dir + lt + '.gbk', 'w')
                    SeqIO.write(lt_context, of, 'genbank')
                    of.close()
