import os
import sys
from operator import itemgetter

colors = []
with open('pubu_colors.txt') as opc:
    for i, line in enumerate(opc):
        if i < 3: continue
        line = line.strip()
        colors.append(line)

data = []
with open('dog_track.txt') as odf:
    for i, line in enumerate(odf):
        if i == 0: continue
        line = line.strip()
        ls = line.split('\t')
        ls[2] = float(ls[2])
        data.append(ls)

col_order = []
og_order = []
dict_data = []
for j, ls in enumerate(sorted(data, key=itemgetter(2), reverse=False)):
    col = colors[j]
    og = ls[0]
    col_order.append('"' + col + '"')
    og_order.append('"' + og + '"')
    dict_data.append('"' + og + '": "' + col + '"')

print('colors <- c(' + ', '.join(col_order) + ')')
print('names(colors) <- c(' + ', '.join(og_order) + ')')
print()
print('colors = {' + ', '.join(dict_data)+  '}')

