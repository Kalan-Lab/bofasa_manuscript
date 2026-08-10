import os
import sys

input_dom_file = sys.argv[1]

with open(input_dom_file) as oidf:
    for i, line in enumerate(oidf):
        line = line.strip('\n')
        ls = line.split('\t')
        if int(ls[1]) >= 20 and  
