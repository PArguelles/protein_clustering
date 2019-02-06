import os
import numpy as np
import MatrixFunctions as mf
from sklearn.preprocessing import MinMaxScaler

def readDistances(measure):
    path_to_matrix = 'C:/ShareSSD/scop2/data_old/sim_'+measure

    counter = 0
    matrix = []

    with open(path_to_matrix, 'r') as fp:

        size = 0
        domains = []

        #get structures
        line = fp.readline()
        while line:
            if 'PDB  :' in str(line): 
                if '#' not in str(line):
                    size += 1
                    domain = str(line).strip().split()[-1].split('/')[-1]
                    domains.append(str(domain))
            if 'Distance records' in str(line):
                break
            line = fp.readline()

        #get distance matrix
        while line:
            if 'DIST :' in str(line): 
                if '#' not in str(line):

                    parsed = str(line).strip().split()
                    current_row = parsed[2]
                    value = float(parsed[4])
            
                    while current_row == parsed[2]:
                    
                        matrix.append(value)
                        line = fp.readline()
                        parsed = str(line).strip().split()
                        value = float(parsed[4])

                    counter += 1

                    i = 0
                    while i < counter:
                        matrix.append(0)
                        i += 1
                    i = 0

                    matrix.append(value)

            line = fp.readline()

    counter += 1

    i = 0
    while i < counter:
        matrix.append(0)
        i += 1
    i = 0

    matrix = np.asmatrix(matrix)
    matrix = matrix.reshape(size,size-1)
    n, _ = matrix.shape 
    X0 = np.zeros((n,1))
    matrix = np.hstack((X0,matrix))

    np.savetxt("C:/ShareSSD/scop2/data_old/kernel_"+measure, matrix, delimiter=' ', newline='\n')

    if 'rmsd' in path_to_matrix:
        matrix = matrix/(matrix.max()/1)

    if 'gdt' in path_to_matrix:
        matrix = mf.processGDTMatrix(matrix)

    matrix = mf.symmetrizeMatrix(matrix)

    np.savetxt("C:/ShareSSD/scop2/data_old/matrix_"+measure, matrix, delimiter=' ', newline='\n')

    return domains, matrix

def readValues(measure):
    path_to_matrix = 'C:/ShareSSD/scop2/data_old/sim_'+measure

    values = []

    with open(path_to_matrix, 'r') as fp:
        line = fp.readline()
        while line:
            if 'DIST :' in str(line): 
                if '#' not in str(line):

                    parsed = str(line).strip().split()
                    value = float(parsed[4])
                    values.append(value)
                    
                    line = fp.readline()

            line = fp.readline()

    values = np.asarray(values)
    
    if 'rmsd' in measure:
        minmax_scaler = MinMaxScaler(feature_range=(0,1))
        values = values.reshape(-1,1)
        values = minmax_scaler.fit_transform(values)

    np.savetxt("C:/ShareSSD/scop2/data_old/kernel_"+measure, values, delimiter=' ', newline='\n')

def loadDomainListFromFile(sample):
    path_to_domains = 'C:/ShareSSD/scop/data_old/domains_'+sample
    domains = []
    with open(path_to_domains, 'r') as fp:
        line = fp.readline()
        while 'END' not in line:
            domains.append(str(line).strip())
            line = fp.readline()
    return domains