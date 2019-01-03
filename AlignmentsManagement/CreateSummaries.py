
import os
import re
import shutil

def createSummaries():

    path_to_alignments = 'C:/ShareSSD/scop2/alignments_maxcluster/'
    path_to_summary = 'C:/ShareSSD/scop2/independent_summary_new'

    visited = set()
    done = set()

    count = 0

    with open(path_to_summary, 'w') as fp:
        for folder in os.listdir(path_to_alignments):
            for filename in os.listdir(path_to_alignments+folder+'/'):
                
                parsed_filename = str(filename).strip().split('-')
                structure1 = parsed_filename[0]
                structure2 = parsed_filename[1]

                if 'gdt-2' in filename and filename not in visited and structure1+' '+structure2 not in done and structure2+' '+structure1 not in done:

                    count += 1

                    #open gdt2 file
                    with open(path_to_alignments+folder+'/'+filename) as nf:
                        line = nf.readline()
                        while line:
                            if 'RMSD' in line:
                                parsed = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                                pairs = parsed[1]
                                rmsd = parsed[2]
                                maxsub1 = parsed[3]
                                length = parsed[4]
                                grmsd = parsed[5]
                                tmscore1 = parsed[6]
                                seq = parsed[7]
                            elif 'GDT=' in line:
                                gdt_2 = re.findall(r"[-+]?\d*\.\d+|\d+", line)[0]
                            line = nf.readline()

                    filename2 = str(filename).replace('gdt-2','gdt-4')

                    #open gdt4 file
                    with open(path_to_alignments+folder+'/'+filename2) as nf2:
                        line = nf2.readline()
                        while line:
                            if 'GDT=' in line:
                                gdt_4 = re.findall(r"[-+]?\d*\.\d+|\d+", line)[0]
                            line = nf2.readline()

                    #open gdt reverse alignment to read tm-score and maxsub
                    filename3 = structure2+'-'+structure1+'-gdt-2'
                    with open(path_to_alignments+structure2+'/'+filename3) as nf3:
                        line = nf3.readline()
                        while line:
                            if 'RMSD' in line:
                                parsed = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                                maxsub2 = parsed[3]
                                tmscore2 = parsed[4]
                            line = nf3.readline()

                    filename4 = filename3.replace('gdt-2','gdt-4')

                    visited.add(filename)
                    visited.add(filename2)
                    visited.add(filename3)
                    visited.add(filename4)
                    done.add(structure1+' '+structure2)
                    done.add(structure2+' '+structure1)

                    print(count)

                    #fp.write(structure1+' '+structure2+' '+rmsd+' '+grmsd+' '+maxsub1+' '+maxsub2+' '+tmscore1+' '+tmscore2+' '+gdt_2+' '+gdt_4+' '+seq+' '+pairs+' '+length)
                    fp.write(structure1+' '+structure2+' '+rmsd+' '+maxsub1+' '+maxsub2+' '+tmscore1+' '+tmscore2+' '+gdt_2+' '+gdt_4+' '+seq+' '+pairs+'\n')

createSummaries()