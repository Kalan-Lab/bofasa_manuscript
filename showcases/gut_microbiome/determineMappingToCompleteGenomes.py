import os
import sys

def determine_og_coord(scaff, start, end, orig_scaff, scaff_offset):
    updated_start = start + scaff_offset - 1 
    updated_end = end + scaff_offset - 1
    updated_coord = tuple([orig_scaff, str(updated_start), str(updated_end)])
    return (updated_coord)

comp_prep_dir = 'Bofasa_Prep_Results/'
gaps_prep_dir = os.path.abspath(sys.argv[1]) + '/'
scaff_map_dir = os.path.abspath(sys.argv[2])+  '/'
map_dir = os.path.abspath(sys.argv[3]) + '/'

comp_bed_dir = comp_prep_dir + 'Genome_Processing/BEDs/'
gaps_bed_dir = gaps_prep_dir + '/Genome_Processing/BEDs/'

for f in os.listdir(comp_bed_dir):
    g = f.split('.bed')[0]

    comp_bed_file = comp_bed_dir + f
    gaps_bed_file = gaps_bed_dir + f
    gappy_map_file = scaff_map_dir + g + '_genomic.fna.mapping'

    gap_scaff_offsets = {}
    with open(gappy_map_file) as ogmf:
        for line in ogmf:
            if line.startswith('#'): continue
            line = line.strip('\n')
            original_seq_id, original_start, original_end, new_seq_id, new_start, new_end = line.split('\t')
            gap_scaff_offsets[new_seq_id] = [original_seq_id, int(original_start)]

    coord_to_lt = {}
    with open(comp_bed_file) as ocbf:
        for line in ocbf:
            line = line.strip('\n')
            ls = line.split('\t')
            # CP102271.1	1	1380	GNPAODLA_00001	0	+
            scaff, start, end, lt, near_edge, strand = ls
            coord = tuple([scaff, start, end])
            coord_to_lt[coord] = lt

    outf = open(map_dir + g + '.txt', 'w')
    with open(gaps_bed_file) as ogbf:
        for line in ogbf:
            line = line.strip('\n')
            ls = line.split('\t')
            scaff, start, end, gappy_lt, near_edge, strand = ls

            coord = determine_og_coord(scaff, int(start), int(end), *gap_scaff_offsets[scaff])
            if coord in coord_to_lt:
                comp_lt = coord_to_lt[coord]
                outf.write(gappy_lt + '\t' + comp_lt + '\n')
    outf.close()
