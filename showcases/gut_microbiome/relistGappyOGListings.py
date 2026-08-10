import os
import sys

gappy_lt_map_dir = os.path.abspath(sys.argv[1]) + '/' # 'Gappy_to_Complete_LT_Mapping/'
og_lt_dir = os.path.abspath(sys.argv[2]) + '/' # 'Gappy_OG_Listings/'
res_dir = os.path.abspath(sys.argv[3]) + '/' # 'Renamed_Gappy_OG_Listings/'

gtc = {}
for f in os.listdir(gappy_lt_map_dir):
    gap_file = gappy_lt_map_dir + f 
    
    with open(gap_file) as ogf:
        for line in ogf:
            line = line.strip('\n')
            ls = line.split('\t')
            gtc[ls[0]] = ls[1]

for f in os.listdir(og_lt_dir):
    og_file = og_lt_dir + f
    res_og_file = res_dir + f
    rof = open(res_og_file, 'w')
    with open(og_file) as oof:
        for line in oof:
            line = line.strip('\n')
            ls = line.split('\t')
            p1, p2 = ls
            
            if p1 in gtc and p2 in gtc:
                rof.write(gtc[p1] + '\t' + gtc[p2] + '\n')
    rof.close()
