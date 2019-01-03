

import os

def sortByStructure():

    #ver se é melhor fazer o sort por id do maxcluster
    path_to_data = 'C:/ShareSSD/scop/gdt_2/summary'
    path_to_sorted = 'C:/ShareSSD/scop/sorted'

    structures = []

    with open(path_to_data, 'r') as fp:

        line = fp.readline()
        while line:
            parsed = str(line).strip().split(' ')
            structures.append((parsed[0],parsed[1],parsed[2]))
            line = fp.readline()

    print(structures)

    structures = sorted(structures, key=lambda x: (x[0], x[1]))

    with open(path_to_sorted,'w') as nf:
        for str1, str2, value in structures:
            nf.write(str1+' '+str2+' '+value+'\n')