import os
import numpy as np
import MatrixFunctions as mf

def readSimilaritiesToMatrix(sample, measure):
    print('Reading distances for '+measure)
    
    path_to_matrix = '/home/pedro/Desktop/scop/data/values_'+sample+'_'+measure
    path_to_domains = '/home/pedro/Desktop/scop/data/domains_'+sample

    counter = 0
    matrix = []
    row = []

    with open(path_to_matrix, 'r') as fp:

        domains = set()

        line = fp.readline()
        while line:

            if 'END' in line:
                break

            parsed = str(line).strip().split(' ')
            structure1 = parsed[0]
            structure2 = parsed[1]
            value = float(parsed[2])

            domains.add(structure1)
            domains.add(structure2)

            # add the respective amount of zeroes to the current row
            counter += 1
            i = 0
            while i < counter:
                row.append(0)
                i += 1
            i = 0

            # track the current structure and read its alignments
            current_row = parsed[0]
            while current_row == parsed[0] and line:
                row.append(value)
                line = fp.readline()
                if 'END' in line:
                    break
                parsed = str(line).strip().split(' ')
                print(parsed)
                value = float(parsed[2])

            matrix.append(row)
            row = []

        line = fp.readline()

    counter += 1

    i = 0
    while i < counter:
        row.append(0)
        i += 1
    i = 0
    matrix.append(row)

    matrix = np.asmatrix(matrix)

    # symmetrize and write results to file
    matrix = mf.symmetrizeMatrix(matrix)
    matrix = np.matrix(matrix)
    matrix.dump("/home/pedro/Desktop/scop/data/matrix_"+sample+'_'+measure)

    # write domain list to file
    if not os.path.isfile(path_to_domains):
        with open(path_to_domains, 'w') as nf:
            domains = list(domains)
            for domain in domains:
                nf.write(domain+'\n')
            nf.write('END')

    #print(matrix)

def loadMatrixFromFile(sample, measure):
    path_to_matrix = '/home/pedro/Desktop/scop/data/matrix_'+sample+'_'+measure
    matrix = np.load(path_to_matrix)
    return matrix

def loadDomainListFromFile(sample):
    path_to_domains = '/home/pedro/Desktop/scop/data/domains_'+sample
    domains = []
    with open(path_to_domains, 'r') as fp:
        line = fp.readline()
        while 'END' not in line:
            domains.append(str(line).strip())
            line = fp.readline()
    return domains

def readMaxsubFile():
    
    path_to_maxsub = '/home/pedro/Desktop/scop2/data_old/maxsubfile'
    path_to_pairs = '/home/pedro/Desktop/scop2/data_old/test_pairs'

    with open(path_to_maxsub, 'r') as fp:
        with open(path_to_pairs, 'w') as fp2:
            line = fp.readline()

            while line:
                if 'MS :' in line:
                    print(line)
                    parsed = str(line).strip().split()
                    if parsed[2] != parsed[3]:
                        fp2.write(parsed[6]+'\n')
                line = fp.readline()

def readRMSDFile():
    path_to_distances = '/home/pedro/Desktop/scop/data/sim_rmsd'
    path_to_new = '/home/pedro/Desktop/scop/data/distances_rmsd'

    with open(path_to_distances, 'r') as fp:
        with open(path_to_new, 'w') as fp2:
            line = fp.readline()

            while line:
                if 'DIST :' in line and '#' not in line:
                    print(line)
                    parsed = str(line).strip().split()
                    if parsed[2] != parsed[3]:
                        fp2.write(parsed[4]+'\n')
                line = fp.readline()
            fp2.write('END')

#juntar pares e distancias com o resto dos dados
def joinDataToFullMatrix():
    path_to_rmsd = '/home/pedro/Desktop/scop/data/distances_rmsd'
    path_to_gdt_2 = '/home/pedro/Desktop/scop/data/distances_gdt_2'
    path_to_gdt_4 = '/home/pedro/Desktop/scop/data/distances_gdt_4'

    path_to_sim = '/home/pedro/Desktop/scop/summary_a.1'
    path_to_newest = '/home/pedro/Desktop/scop/newest_sum'

    with open(path_to_sim,'r') as fp:
        with open(path_to_rmsd, 'r') as fp2:
            with open(path_to_gdt_2, 'r') as fp3:
                with open(path_to_gdt_4, 'r') as fp4:
                    with open(path_to_newest, 'w') as fp5:

                        line = fp.readline()
                        line2 = fp2.readline()
                        line3 = fp3.readline()
                        line4 = fp4.readline()

                        while line:

                            parsed = str(line).strip().split()
                            rmsd = str(line2).strip().split()[0]
                            gdt2 = str(line3).strip().split()[0]
                            gdt4 = str(line4).strip().split()[0]

                            # structure1 structure2 rmsd maxsub1 maxsub2 tmscore1 tmscore2 gdt_2 gdt_4 seq_id pairs
                            to_write = parsed[0]+' '+parsed[1]+' '+rmsd+' '+parsed[3]+' '+parsed[4]+' '+parsed[5]+' '+parsed[6]+' '+gdt2+' '+gdt4+' '+parsed[9]+' '+parsed[10]+'\n'
                            print(to_write)
                            fp5.write(to_write)

                            line = fp.readline()
                            line2 = fp2.readline()
                            line3 = fp3.readline()
                            line4 = fp4.readline()
