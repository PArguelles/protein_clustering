

import os

def getBestScores():

    path_to_results = 'C:/ShareSSD/scop/clustering_results_single/'

    _algorithm = ''
    _measure1 = ''
    _measure2 = ''
    _homogeneity = 0
    _completeness = 0
    _vm = 0
    _ari = 0
    _ami = 0
    _ch = 0
    _sc = 0

    sample = 'a.1.'

    for filename in os.listdir(path_to_results):
        
        parsed_filename = str(filename).split('_')

        algorithm = parsed_filename[0]
        measure1 = parsed_filename[-2]
        measure2 = parsed_filename[-1]

        if sample in filename:

            with open(path_to_results+filename) as fp:
                
                line = fp.readline()
                while line:

                    parsed_line = str(line).strip().split()
                    if 'Homogeneity' in line:
                        homogeneity = float(parsed_line[-1])
                    if 'Completeness' in line:
                        completeness = float(parsed_line[-1])
                    if 'V-measure' in line:
                        vm = float(parsed_line[-1])
                    if 'Adjusted Rand Index' in line:
                        ari = float(parsed_line[-1])
                    if 'Adjusted Mutual Information' in line:
                        ami = float(parsed_line[-1])
                    if 'Calinksi-Harabaz' in line:
                        ch = float(parsed_line[-1])
                    if 'Silhouette coefficient' in line:
                        sc = float(parsed_line[-1])

                    line = fp.readline()

            if sc > _sc:
                _homogeneity = homogeneity
                _completeness = completeness
                _vm = vm
                _ari = ari
                _ami = ami
                _ch = ch
                _sc = sc
                _algorithm = algorithm
                _measure1 = measure1
                _measure2 = measure2

    print(_algorithm+'_'+_measure1+'_'+_measure2)
    print(_homogeneity)
    print(_completeness)
    print(_vm)
    print(_ari)
    print(_ami)
    print(_ch)
    print(_sc)


getBestScores()