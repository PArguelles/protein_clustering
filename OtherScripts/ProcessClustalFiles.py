
import numpy as np

def processClustalFiles(sample):

    path_to_matrix = 'C:/ShareSSD/scop/sequences_'+sample+'pim'
    path_to_new = 'C:/ShareSSD/scop/matrix_'+sample+'_seq'

    matrix = []

    with open(path_to_matrix, 'r') as fp:

        with open(path_to_new, 'w') as fp2:

            line = fp.readline()

            while line:

                if ':' in line:
                    
                    parsed = str(line).strip().split()
                    parsed = [float(i) for i in parsed[2:]]
                    matrix.append(parsed)
                    print(parsed[2:])

                    print(line)


                line = fp.readline()
        
        final = np.matrix(matrix)
        
        print(final)
        final.dump(path_to_new)
        #np.savetxt(path_to_new,final,delimiter=' ', newline='\n')

processClustalFiles('a.1.')
processClustalFiles('a.3.')
processClustalFiles('b.2.')
processClustalFiles('b.3.')