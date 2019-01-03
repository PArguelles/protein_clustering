

import os
import re

def getStructureIds():
    path_to_matrix = 'C:/ShareSSD/scop/data/sim_gdt2'
    mappings = {}
    with open(path_to_matrix, 'r') as fp:
        line = fp.readline()
        while line:
            if 'PDB  :' in line and '#' not in line:
                structure = str(line).strip().split()[-1].split('/')[-1]
                id = str(line).strip().split()[2]
                mappings[id] = structure
            line = fp.readline()
    return mappings

def getToDoLines(mappings):

    path_to_matrix = 'C:/ShareSSD/scop/data/sim_gdt2'
    path_to_todo = 'C:/ShareSSD/scop2/todo_list'

    with open(path_to_matrix, 'r') as fp:
        with open(path_to_todo, 'w') as nf:
            line = fp.readline()
            while line:

                if 'DIST :' in line and '#' not in line:

                    parsed = str(line).strip().split()
                    print(parsed)
                    id1 = parsed[2]
                    id2 = parsed[3]

                    nf.write(mappings[id1]+' '+mappings[id2]+'\n')

                line = fp.readline()

#usar este para fazer sumarios
def createSummaries():

    path_to_todo = 'C:/ShareSSD/scop2/todo_list'
    path_to_alignments = 'C:/ShareSSD/scop2/alignments_maxcluster/'
    path_to_summary = 'C:/ShareSSD/scop2/new_summary'
    path_to_skipped = 'C:/ShareSSD/scop2/skipped'

    count = 0

    with open(path_to_summary, 'w') as nf:
        with open(path_to_skipped, 'w') as nf2:
            with open(path_to_todo, 'r') as fp:
                
                line = fp.readline()
                while line:

                    print(count)
                    count += 1

                    parsed = str(line).strip().split(' ')
                    structure1 = parsed[0]
                    structure2 = parsed[1]

                    try:

                        #GDT-2
                        filename = structure1+'-'+structure2+'-gdt-2'
                        with open(path_to_alignments+structure1+'/'+filename) as fp2:
                            line2 = fp2.readline()
                            while line2:
                                if 'RMSD' in line2:
                                    parsed = re.findall(r"[-+]?\d*\.\d+|\d+", line2)
                                    pairs = parsed[1]
                                    rmsd = parsed[2]
                                    maxsub1 = parsed[3]
                                    length = parsed[4]
                                    grmsd = parsed[5]
                                    tmscore1 = parsed[6]
                                    seq = parsed[7]
                                elif 'GDT=' in line2:
                                    gdt_2 = re.findall(r"[-+]?\d*\.\d+|\d+", line2)[0]
                                line2 = fp2.readline()

                        #GDT-4
                        filename2 = str(filename).replace('gdt-2','gdt-4')
                        with open(path_to_alignments+structure1+'/'+filename2) as fp3:
                            line2 = fp3.readline()
                            while line2:
                                if 'GDT=' in line2:
                                    gdt_4 = re.findall(r"[-+]?\d*\.\d+|\d+", line2)[0]
                                    break
                                line2 = fp3.readline()

                        #REVERSE
                        filename3 = structure2+'-'+structure1+'-gdt-2'
                        with open(path_to_alignments+structure2+'/'+filename3) as fp4:
                            line2 = fp4.readline()
                            while line2:
                                if 'RMSD=' in line2:
                                    parsed = re.findall(r"[-+]?\d*\.\d+|\d+", line2)
                                    maxsub2 = parsed[3]
                                    tmscore2 = parsed[6]
                                    break
                                line2 = fp4.readline()

                        #WRITE DATA TO SUMMARY
                        print(structure1+' '+structure2+' '+rmsd+' '+maxsub1+' '+maxsub2+' '+tmscore1+' '+tmscore2+' '+gdt_2+' '+gdt_4+' '+seq+' '+pairs+'\n')
                        nf.write(structure1+' '+structure2+' '+rmsd+' '+maxsub1+' '+maxsub2+' '+tmscore1+' '+tmscore2+' '+gdt_2+' '+gdt_4+' '+seq+' '+pairs+'\n')

                    except Exception:
                        nf2.write(structure1+' '+structure2+'\n')

                    line = fp.readline()

def appendMaxsubPairs():
    path_to_summary = 'C:/ShareSSD/scop2/full_similarity_matrix_a.1'
    path_to_newest_summary = 'C:/ShareSSD/scop2/updated_summary'
    path_to_alignments = 'C:/ShareSSD/scop2/alignments_maxcluster/'
    path_to_skipped = 'C:/ShareSSD/scop2/skipped_new'

    count = 0

    with open(path_to_summary, 'r') as fp:
        with open(path_to_newest_summary, 'w') as fp2:
            with open(path_to_skipped, 'w') as fp4:
                
                line = fp.readline()
                while line:

                    print(count)
                    count += 1

                    parsed = str(line).strip().split()
                    structure1 = parsed[0]
                    structure2 = parsed[1]

                    try:
                        #read maxsub pairs
                        with open(path_to_alignments+structure1+'/'+structure1+'-'+structure2+'-gdt-2', 'r') as fp3:
                            pairs = re.findall(r"[-+]?\d*\.\d+|\d+", fp3.readline())[1]

                        line_to_write = str(line).strip()+' '+str(pairs)+'\n'
                        fp2.write(line_to_write)
                        print(line_to_write)

                    except Exception:
                    
                        fp4.write(structure1+' '+structure2+'\n')

                    line = fp.readline()

appendMaxsubPairs()