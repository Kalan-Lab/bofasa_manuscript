import os
import sys

showcase_dir = '../../showcases/'
for i, sc in enumerate(os.listdir(showcase_dir)):
    trf = showcase_dir + sc + '/Timing_and_Resources.txt'
    with open(trf) as otf:
        for j, line in enumerate(otf):
            line = line.strip()
            ls = line.split('\t')
            if i == 0:
                if j == 0:
                    print('showcase\tmethod_color\t' + line)
                else:
                    print(sc + '\t' + ls[0].split()[0] + '\t' + line)
            elif i > 0:
                if j != 0:
                    print(sc + '\t' + ls[0].split()[0] + '\t' + line)

            
