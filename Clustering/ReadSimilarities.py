import os
import numpy as np
import MatrixFunctions as mf
from sklearn.preprocessing import MinMaxScaler


def readSimilaritiesToMatrix(sample, measure):
    
    path_to_matrix = 'C:/ShareSSD/scop/data/values_'+sample+'_'+measure
    path_to_domains = 'C:/ShareSSD/scop/data/domains_'+sample

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
    matrix.dump("C:/ShareSSD/scop/data/matrix_"+sample+'_'+measure)

    # write domain list to file
    if not os.path.isfile(path_to_domains):
        with open(path_to_domains, 'w') as nf:
            domains = list(domains)
            for domain in domains:
                nf.write(domain+'\n')
            nf.write('END')

    #print(matrix)

def loadMatrixFromFile(sample, measure):
    path_to_matrix = 'C:/ShareSSD/scop/data/matrix_'+sample+'_'+measure
    matrix = np.load(path_to_matrix)
    return matrix

def loadDomainListFromFile(sample):
    path_to_domains = 'C:/ShareSSD/scop/data/domains_'+sample
    domains = []
    with open(path_to_domains, 'r') as fp:
        line = fp.readline()
        while 'END' not in line:
            domains.append(str(line).strip())
            line = fp.readline()
    return domains

def readMaxsubFile():
    
    path_to_maxsub = 'C:/ShareSSD/scop2/data_old/maxsubfile'
    path_to_pairs = 'C:/ShareSSD/scop2/data_old/test_pairs'

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
    path_to_distances = 'C:/ShareSSD/scop/data/sim_gdt2'
    path_to_new = 'C:/ShareSSD/scop/data/distances_gdt_2'

    with open(path_to_distances, 'r') as fp:
        with open(path_to_new, 'w') as fp2:
            line = fp.readline()

            while line:
                if 'DIST :' in line:
                    print(line)
                    parsed = str(line).strip().split()
                    if parsed[2] != parsed[3]:
                        fp2.write(parsed[4]+'\n')
                line = fp.readline()
            fp2.write('END')

# readsimilaritiestomatrix('a.1.', 'rmsd')
# readsimilaritiestomatrix('a.1.', 'gdt_2')
# readsimilaritiestomatrix('a.1.', 'gdt_4')
# readsimilaritiestomatrix('a.3.', 'rmsd')
# readsimilaritiestomatrix('a.3.', 'gdt_2')
# readsimilaritiestomatrix('a.3.', 'gdt_4')
# readsimilaritiestomatrix('b.2.', 'rmsd')
# readsimilaritiestomatrix('b.2.', 'gdt_2')
# readsimilaritiestomatrix('b.2.', 'gdt_4')
# readsimilaritiestomatrix('b.3.', 'rmsd')
# readsimilaritiestomatrix('b.3.', 'gdt_2')
# readsimilaritiestomatrix('b.3.', 'gdt_4')
