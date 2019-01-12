

import os

with open('C:/ShareSSD/scop/structure_list','r') as fp:
    with open('C:/ShareSSD/scop/structure_list_new','w') as fp2:
        line = fp.readline()
        while line:

            structure = str(line).strip().split()[0]

            fp2.write('C:/ShareSSD/scop/structures/'+structure+'\n')

            line = fp.readline()