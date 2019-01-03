


import os

def splitData(measure_name, column):

    path_to_summary = 'C:/ShareSSD/scop/summary_a.1._new'

    path_to_new = 'C:/ShareSSD/scop/data/values_'+measure_name

    with open(path_to_summary, 'r') as fp:
        with open(path_to_new, 'w') as nf:

            line = fp.readline()
            while line:

                parsed = str(line).strip().split()
                print(parsed)
                structure1 = parsed[0]
                structure2 = parsed[1]
                value = parsed[column]

                # structure1 structure2 rmsd maxsub1 maxsub2 tmscore1 tmscore2 gdt_2 gdt_4 seq_id pairs
                nf.write(structure1+' '+structure2+' '+value+'\n')
                line = fp.readline()

def splitDataMaxsub(measure, column, signal):

    path_to_summary = 'C:/ShareSSD/scop2/data/full_summary_a.1'
    path_to_new = 'C:/ShareSSD/scop2/data/values_'+measure

    with open(path_to_summary, 'r') as fp:
        with open(path_to_new, 'w') as nf:

            line = fp.readline()
            while line:

                parsed = str(line).strip().split()
                print(parsed)
                structure1 = parsed[0]
                structure2 = parsed[1]
                value1 = parsed[column]
                value2 = parsed[column+1]

                if signal == True:
                    if value1 > value2:
                        value = value1
                    else:
                        value = value2
                elif signal == False:
                    if value1 < value2:
                        value = value1
                    else:
                        value = value2

                # structure1 structure2 rmsd maxsub1 maxsub2 tmscore1 tmscore2 gdt_2 gdt_4 seq pairs
                nf.write(structure1+' '+structure2+' '+value+'\n')
                line = fp.readline()
