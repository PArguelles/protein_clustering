
import os
import re

path_to_tmalign = 'C:/ShareSSD/scop2/tmalign/'
path_to_maxcluster = 'C:/ShareSSD/scop2/redo/'
path_to_new = 'C:/ShareSSD/scop2/tmalign_maxcluster/'

count = 0

for filename in os.listdir(path_to_maxcluster):

    print(count)
    count += 1

    parsed = str(filename).split('-')
    structure1 = parsed[0]
    structure2 = parsed[1]
    measure = parsed[-1]

    #read maxcluster files
    with open(path_to_maxcluster+filename, 'r') as fp:
        line = fp.readline()
        while line:
            if 'RMSD' in line:
                rmsd_line = str(line).strip()
            if 'GDT=' in line:
                gdt_line = str(line)
            line = fp.readline()

    filename = structure1+'-'+structure2+'-tm'
    with open(path_to_tmalign+filename, 'r') as fp2:
        line = fp2.readline()
        while line:
            if 'Seq_ID=' in line:
                seq_id = re.findall(r"[-+]?\d*\.\d+|\d+", line)[2]
            line = fp2.readline()

    new = str(structure1)+'-'+str(structure2)+'-gdt-'+str(measure)
    with open(path_to_new+new, 'w') as nf:
        nf.write(rmsd_line+', %ID=  '+seq_id+'\n')
        nf.write(gdt_line+'\n')