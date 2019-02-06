import os
import numpy as np
import MatrixFunctions as mf
from sklearn.preprocessing import MinMaxScaler

def getValidFilesFromList():
    path_to_file = 'C:/ShareSSD/scop/testmax'
    path_to_valid = 'C:/ShareSSD/scop/valid_structures'

    pattern = '/home/pedro/ShareSSD/scop/structures/'
    stop = 'INFO  : Cluster  Centroid  Size        Spread'

    with open(path_to_valid, 'w') as nf:
        with open(path_to_file, 'r') as fp:
            line = fp.readline()
            while line and stop not in line:
                if pattern in line:
                    nf.write(line[-12:-1]+'\n')
                line = fp.readline()

def readDistances(sample, measure):
    path_to_matrix = 'C:/ShareSSD/scop/data_old/sim_'+sample+'_'+measure

    counter = 0
    matrix = []

    with open(path_to_matrix, 'r') as fp:

        size = 0
        domains = []

        #get number of structures
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
                    print(line)
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

    #np.savetxt("C:/ShareSSD/scop/data_old/matrix2.txt", matrix,delimiter=' ', newline='\n')

    #if 'rmsd' in path_to_matrix:
        #matrix = matrix/(matrix.max()/1)

    matrix = mf.symmetrizeMatrix(matrix)

    #if 'gdt' in path_to_matrix:
        #matrix = mf.processGDTMatrix(matrix)

    #np.savetxt("C:/ShareSSD/scop/data_old/matrix3.txt", matrix,delimiter=' ', newline='\n')

    return domains, matrix

def loadMatrixFromFile(sample, measure):
    path_to_matrix = 'C:/ShareSSD/scop/data/matrix_'+sample+'_'+measure
    matrix = np.load(path_to_matrix)
    return matrix

def readKernelParameters(sample, measure):
    path_to_stats = 'C:/ShareSSD/scop/data/stats_'+sample+'_'+measure
    with open(path_to_stats, 'r') as fp:
        line = fp.readline()
        while line:
            value = str(line).strip().split()[0]
            if 'Mean' in line:
                mean = value
            elif 'Standard deviation' in line:
                std_dev = value
            elif 'Variance' in line:
                variance = value
            line = fp.readline()
    return mean, std_dev, variance

def readDistancesMaxsub(measure):
    #path_to_matrix = 'C:/ShareSSD/scop2/data_old/'+measure+'file'
    path_to_matrix = 'C:/ShareSSD/scop/data_old/testfile'
    counter = 0
    matrix = []

    with open(path_to_matrix, 'r') as fp:

        size = 0
        domains = []

        #get number of structures
        line = fp.readline()
        while line:
            if 'PDB  :' in str(line): 
                if '#' not in str(line):
                    size += 1
                    domain = str(line).strip().split()[-1].split('/')[-1]
                    domains.append(str(domain))
            if 'Maxsub records' in str(line):
                break
            line = fp.readline()

        #get distance matrix
        while line:
            if 'MS :' in str(line): 
                if '#' not in str(line):

                    parsed = str(line).strip().split()

                    current_row = parsed[2]
                    value = float(parsed[5])
            
                    while current_row == parsed[2]:
                    
                        matrix.append(value)
                        line = fp.readline()
                        parsed = str(line).strip().split()
                        value = float(parsed[5])

                    matrix.append(value)

            line = fp.readline()

    counter += 1

    matrix = np.asmatrix(matrix)
    matrix = matrix.reshape(size,size-1)
    n, _ = matrix.shape 
    X0 = np.zeros((n,1))
    matrix = np.hstack((X0,matrix))

    np.savetxt("C:/ShareSSD/scop2/data_old/matrix2.txt", matrix,delimiter=' ', newline='\n')

    if 'rmsd' in path_to_matrix:
        matrix = matrix/(matrix.max()/1)

    matrix = mf.symmetrizeMatrix(matrix)

    if 'gdt' in path_to_matrix:
        matrix = mf.processGDTMatrix(matrix)

    np.savetxt("C:/ShareSSD/scop2/data_old/matrix3.txt", matrix,delimiter=' ', newline='\n')

    return domains, matrix