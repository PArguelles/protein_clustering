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

#juntar pares e distancias com o resto dos dados
def joinDataToFullMatrix():
    path_to_rmsd = 'C:/ShareSSD/scop/data/distances_rmsd'
    path_to_gdt_2 = 'C:/ShareSSD/scop/data/distances_gdt_2'
    path_to_gdt_4 = 'C:/ShareSSD/scop/data/distances_gdt_4'

    path_to_sim = 'C:/ShareSSD/scop/summary_a.1'
    path_to_newest = 'C:/ShareSSD/scop/newest_sum'

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


joinDataToFullMatrix()
